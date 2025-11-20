import os

from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_KEY = os.getenv('OPENROUTER_KEY')


def get_model_client():
    model_client = OpenAIChatCompletionClient(
        base_url="https://openrouter.ai/api/v1",
        model="x-ai/grok-4.1-fast",
        api_key=os.getenv("OPENROUTER_KEY"),
        model_info={
            "family": "x-ai",
            "vision": True,
            "function_calling": True,
            "json_output": False
        }
    )

    return model_client
