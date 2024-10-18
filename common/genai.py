from enum import Enum
from typing import Dict, Union
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models.base import BaseChatModel
from langchain_core.runnables import RunnableSerializable
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from common.model import Quiz
from loguru import logger


class Provider(str, Enum):
    GOOGLE = "google"

class LLM(str, Enum):
    GEMINI_1o5_FLASH="gemini-1.5-flash"
    GEMINI_1o5_PRO="gemini-1.5-pro"


class ModelGateway:
    provider_model_map: Dict[Provider, Dict[LLM, BaseModel]] = {
        Provider.GOOGLE: {
            "supported_models": [LLM.GEMINI_1o5_FLASH, LLM.GEMINI_1o5_PRO],
            "langchain_adapter": ChatGoogleGenerativeAI
        }
    }
    @classmethod
    def get_adapter(
        cls,
        provider: Provider,
        model: LLM,
        **kwargs
    ) -> Union[BaseChatModel]:
        """
        Returns an initialized langchain adapter for the given provider and model where any passed kwargs are passed to the adapter such as temperature, top_p, etc.
        """
        return cls.provider_model_map[provider]["langchain_adapter"](model=model, **kwargs)


def init_quiz_generator_chain(
    provider: Provider,
    model: LLM,
    prompt_template: str,
    prompt_name: str
) -> RunnableSerializable:
    """
    Initializes a langchain chain for generating a quiz based on the given provider and model and prompt template. To view the LLM run with the observability tool built-in with Langchain, go to https://smith.langchain.com/ and follow the quickstart instructions. No extra setup is required.
    
    For advanced users, the Prompt Template declaration automatically formats the format instructions per the pydantic model for the quiz. We can change the properties of the returned output by modifying the pydantic model. Extra KWARGS passed onto the model adapter also applies to the langchain BaseChatModel, e.g, passing temperature and other kwargs to the model adapter.
    
    - When connecting an OPENAI Model, we can enable JSON Mode by passing a model_config kwarg that is designed for the adapter which passes onto the base OpenAI model. Think of any kwarg from the top level model gateway -> adapter -> OpenAI().client.chat.completions.create(...)
    
    `model_kwargs = {"response_format": {"type": "json_object"}}`
    
    
    Params:
        provider (Enum): The provider to use for the quiz generator
        model (Enum): The model to use for the quiz generator
        prompt_template (str): The prompt template to use for the quiz generator
    
    Returns:
        RunnableSerializable: A runnable langchain chain for generating a quiz
    """
    logger.debug(f"Creating LLM call with prompt: {prompt_name}")
    parser = PydanticOutputParser(pydantic_object=Quiz)
    prompt = PromptTemplate(
        template = prompt_template,
        input_variables = ["input"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )
    chain = (
        prompt
        | ModelGateway.get_adapter(provider, model, temperature=0)
        | parser
    ).with_config({"run_name": f"Quiz Generator - {prompt_name}"})
    logger.debug(f"Formatted Prompt Preview: {prompt.format(input='test')}")
    return chain
