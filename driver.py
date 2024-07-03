from fastapi import FastAPI, Body
import util,json
from prompts import IntentPrompt

# Example usage:
prompt_instance = IntentPrompt()
with open("prompts.json", "r") as file:
    # Parse the JSON data
    promptLibrary = json.load(file)

app = FastAPI()


@app.get("/")
def landing_page():
    return {"message": "Welcome to Azure Region " + util.SPEECH_REGION}


@app.post("/extract_intent")
def llm_text(newD=Body()):
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


@app.get("/extract_intent_from_voice_and_interact")
def llm_voice():

    try:

        options = ["en-US", "ja-JP"]
        targetJSON = {}
        


        #1. Greet the user on call.
        util.respondtoUser("How may I assist you.")

        #2. Extract the users audio and do STT
        userCall = util.recognize_from_microphone(options[0])
        
        #3. Create relevant prompt
        userIntent = util.prompt_Creation(
            userCall, prompt_instance.USER_INTENT_PROMPT, 0.1
        )

        #4. GENERATE A CONTEXTUAL RESPONSE
        contextualresponse = util.prompt_Creation(
            userCall,prompt_instance.EMPATHY, 0.1
        )

        #5. Respond to the user
        util.respondtoUser(contextualresponse)


        #6. Extract KYC
        util.respondtoUser("Let me help you, just share some details with me.")

        masterQuestionKeyPhrases = ['name','date of birth','policy number']

        keyValPair = {}
        for qes in masterQuestionKeyPhrases:
            keyValPair[qes] = util.prompt_to_question(qes)

        
        targetJSON['USER_INTENT'] = userIntent

        for key,ques in keyValPair.items():
            # Run the loop to extract the values
            util.respondtoUser(ques)

            rawAnswer = util.recognize_from_microphone(options[0])
            keyPhraseExtracted = util.extractKeyPhrase(key,rawAnswer)

            targetJSON[key] = keyPhraseExtracted
        return targetJSON
    
    except Exception as e:
        exception_message = str(e)
        return exception_message