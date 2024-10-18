# prompt-engineering
Template Repository for the Journey 1 Prompt Engineering mission demonstrating how prompting and structured instructions can affect outputs.

### Overview
This is a Python project demonstrating how prompting and structured instructions can affect outputs. It uses different techniques to generate AI prompts.

## Project Structure

The project is structured as follows:

- `main.py`: This is the main entry point of the application.
- `common/`: This directory contains the core modules of the application:
  - `controller.py`: Handles the application logic.
  - `genai.py`: Contains the AI generation logic.
  - `model.py`: Defines the data models.
  - `view.py`: Handles the user interface.
- `prompts/`: This directory contains different techniques for generating prompts:
  - `chain_of_thought.py`: Implements the Chain of Thought technique.
  - `examples.py`: Provides examples.
  - `few_shot.py`: Implements the Few-Shot technique.
  - `zero_shot.py`: Implements the Zero-Shot technique.

## Getting Started

1. Clone the repository:

```sh
git clone https://github.com/yourusername/prompt-engineering.git
```

2. Navigate to the project directory

```sh
cd prompt-engineering
```

3. Install the required dependencies:

```sh
pip install -r requirements.txt
```

4. Run the application:

```sh
streamlit run main.py
```

5. Open the application in your browser at http://localhost:8501.

### Usage
To use a specific prompt technique, import the `PROMPT_TECHNIQUES` dictionary from the `prompts` module and pass the desired technique as a key. For example, to use the Zero-Shot technique, you can do the following:

```python
from prompts import PROMPT_TECHNIQUES

prompt_template = PROMPT_TECHNIQUES["Zero-Shot"]
```

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
