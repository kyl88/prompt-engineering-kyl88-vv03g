from pydantic import BaseModel, Field, model_validator
from enum import Enum


class Views(str, Enum):
    REQUEST = "request"
    QUIZ = "quiz"
    RESULTS = "results"


class Choice(BaseModel):
    key: str = Field(..., description="The key for the choice which exists as a single character as a key")
    value: str = Field(..., description="The value for the choice")
    
    def __str__(self):
        return f"{self.key}) {self.value}"


class Question(BaseModel):
    question: str = Field(..., description="The question to be asked")
    choices: list[Choice] = Field(..., description="The choices for the question")
    answer: str = Field(..., description="The answer to the question. Validated against choices to ensure answer exists in the choices list based on the key. Exists as a single character as a key.")
    
    @model_validator(mode="after")
    def validate_answer(self):
        if self.answer not in [c.key for c in self.choices]:
            raise ValueError("Answer must be one of the choices")
        return self

    @model_validator(mode="after")
    def validate_answer_str(self):
        if len(self.answer) > 1:
            raise ValueError("Answer must be a single character as a key")
        return self

    def __str__(self):
        return f"{self.question}\n{[c.__str__ for c in self.choices]}"


class Quiz(BaseModel):
    questions: list[Question] = Field(..., description="The questions for the quiz")