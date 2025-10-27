import os

from dotenv import load_dotenv
from agents.extensions.models.litellm_model import LitellmModel


load_dotenv()


MODEL = os.getenv("MODEL_NAME", "gpt-5-mini")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")

if not BASE_URL or not API_KEY:
    raise ValueError("BASE_URL and API_KEY must be set in environment variables.")

lite_llm_model_config = LitellmModel(
    model=MODEL,
    base_url=BASE_URL,
    api_key=API_KEY,
)