from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

chatgpt_api_key = os.getenv('SPEECH_REGION')