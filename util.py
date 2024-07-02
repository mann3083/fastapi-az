from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

SPEECH_REGION = os.getenv('SPEECH_REGION')