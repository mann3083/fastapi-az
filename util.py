from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()  # take environment variables from .env.

SPEECH_REGION = os.getenv('SPEECH_REGION')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
endpoint = os.getenv('endpoint')
key = os.getenv('key')
client = OpenAI(api_key=OPENAI_API_KEY)

def prompt_Creation(query, prmpt, temp=0.1):

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prmpt},
            {"role": "user", "content": query},
        ],
        max_tokens=75,  # Limit the maximum length of the generated question
        temperature=temp,  # Controls the randomness of the generated text
        n=1,  # Generate only one response
        stop=None,  # Stop generation at a specific token
    )
    return response.choices[0].message.content