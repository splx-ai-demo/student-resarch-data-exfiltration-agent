import os

from agents import OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

load_dotenv()

AZURE_KEY = os.getenv("AZURE_OPENAI_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

if not all([AZURE_KEY, AZURE_ENDPOINT, AZURE_API_VERSION, AZURE_DEPLOYMENT_NAME]):
    raise ImportError(
        "Azure credentials not found. Please set AZURE_OPENAI_KEY, "
        "AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_API_VERSION, and "
        "AZURE_OPENAI_DEPLOYMENT_NAME in your .env file."
    )

azure_client = AsyncAzureOpenAI(
    api_key=AZURE_KEY, api_version=AZURE_API_VERSION, azure_endpoint=AZURE_ENDPOINT
)

azure_model_config = OpenAIChatCompletionsModel(
    model=AZURE_DEPLOYMENT_NAME,
    openai_client=azure_client,
)
