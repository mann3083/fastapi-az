from fastapi import FastAPI, Body
import util
from prompts import IntentPrompt

# Example usage:
prompt_instance = IntentPrompt()

app = FastAPI()


@app.get("/")
def simpleGet():
    return {"message": "Welcome to Azure Region " + util.SPEECH_REGION}


@app.post("/insert")
def simplepost(newD=Body()):
    userQuery = newD["query"]
    options = ["en-US", "ja-JP"]
    # Make the call to open api and get a response.
    # userCall = util.recognize_from_microphone(options[0])
    # util.respondtoUser("Hello! Welcome to Kaizen Cliams - How may I assist you.")
    try:
        userIntent = util.prompt_Creation(
            userQuery, prompt_instance.USER_INTENT_PROMPT, 0.1
        )

        return userIntent
    except Exception as e:
        exception_message = str(e)
        return exception_message
