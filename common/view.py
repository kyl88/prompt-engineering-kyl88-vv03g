from common.model import Views, Question
from streamlit import session_state as ss
import streamlit as st
from loguru import logger


class View:
    """
    Primary responsibility to handle streamlit rendering and pass interactions to the controller from the user. Utilizes the models to help render outputs like the quiz. 
    
    Functions as exposing API to the controller to render and handle user interactions.
    """
    def __init__(self):
        """
        The self.pc is a multi-element container holding two elements: A title and the canvas. We utilize an empty container (a streamlit single element container) to 'clear' the container and can update the canvas with new content. When calling changes to the primary container, use the update canvas method to pass a single parent element to the canvas and optionally update the title.
        """
        if 'current_view' not in ss:
            ss.current_view = Views.REQUEST
        if 'lock' not in ss:
            ss.lock = False
        self.canvas = st.container(border=True)
        self.canvas.empty()
        self.current_view = ss.current_view
    
    
    def render(self, controller):
        view_methods = {
            Views.REQUEST: self.render_request_view,
            Views.QUIZ: self.render_quiz_view,
            Views.RESULTS: self.render_results_view
        }
        view_method = view_methods.get(self.current_view)
        if view_method:
            logger.debug(f"Rendering view: {self.current_view}")
            view_method(controller)
        else:
            raise ValueError(f"Unknown view type: {self.current_view}")
    
    
    # Render Methods for each view
    def render_request_view(self, controller):
        container = self.canvas.empty()
        
        if ss.current_view == Views.REQUEST:
            form = container.form('request_form', border=False)
            form.title("Generate Quiz")
            
            topic = form.text_input('Enter a topic for the quiz: ')
            generate = form.form_submit_button('Generate')
            
            if generate:
                with st.spinner("Generating quiz..."):
                    if topic == "": form.error("Please enter a topic")
                    else:
                        controller.set_view(self)
                        controller.generate_quiz(
                            model=ss.model,
                            provider=ss.provider,
                            topic=topic,
                            prompt_template=ss.current_prompt
                        )
                        container.empty()
        else:
            container.error(f"View method render request but current view is not request, got {ss.current_view}")


    def render_quiz_view(self, controller):
        def lock_toggle():
            ss.lock = not ss.lock
        
        container = self.canvas.empty()
        form = container.form('quiz_form', border=False)
        form.title("Quiz")
        
        if ss.current_view == Views.QUIZ and 'quiz' in ss and 'current_question_index' in ss:
            locked = ss.get('lock', False)
            question: Question = ss.quiz.questions[ss.current_question_index]
            form.write(question.question)
            
            choice = form.radio(
                "Select your answer",
                [c for c in question.choices],
                disabled=locked
            )
            
            quiz_submit = form.form_submit_button("Submit", disabled=locked, on_click=lock_toggle)
            
            if quiz_submit:
                controller.set_view(self)
                is_correct = controller.answer_question(choice.key, question)
                self.show_answer_feedback(is_correct)
                controller.handle_quiz_progression()
                self.canvas.empty()
            
            if ss.lock and ss.answered_question and not quiz_submit:
                controller.set_view(self)
                index = ss.current_question_index
                if index+1 >= len(ss.quiz.questions):
                    self.show_results()
                else:
                    self.show_next_question()
            
        else:
            form.error("Quiz has not been generated")

    
    def render_results_view(self, controller):
        container = self.canvas.empty()
        
        correct = ss.get('total_correct', 0)
        incorrect = ss.get('total_incorrect', 0)
        
        form = container.form(f'results_form', border=False)
        
        if ss.current_view == Views.RESULTS:
            form.title("Results")
            form.write(f"Total Correct: {correct}")
            form.write(f"Total Incorrect: {incorrect}")
            form.form_submit_button("Create New Quiz", on_click=self.reset_all_callback)
            
        else:
            form.error("View method render results but current view is not results")
    
    
    #################################
    # Util Methods for handling view logic
    def show_answer_feedback(self, is_correct):
        if 'total_correct' not in ss or 'total_incorrect' not in ss:
            ss.total_correct = 0
            ss.total_incorrect = 0
        
        if is_correct:
            st.success("Correct!")
            ss.total_correct += 1
        else:
            st.error("Incorrect")
            ss.total_incorrect += 1
    
    def unlock_callback(self):
        ss.lock = False
    
    def show_next_question(self):
        progression = self.canvas.form('progression_form', border=False)
        _next = progression.form_submit_button("Next", on_click=self.unlock_callback)

    def show_results_callback(self):
        ss.current_view = Views.RESULTS

    def show_results(self):
        end_quiz = self.canvas.form('end_quiz_form', border=False)
        _end = end_quiz.form_submit_button("End Quiz", on_click=self.show_results_callback)

    def reset_all_callback(self):
        ss.current_view = Views.REQUEST
        ss.quiz = None
        ss.current_question_index = 0
        ss.total_correct = 0
        ss.total_incorrect = 0
        ss.lock = False
