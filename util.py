from dotenv import load_dotenv
from openai import OpenAI
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import azure.cognitiveservices.speech as speechsdk
from prompts import IntentPrompt

load_dotenv()  # take environment variables from .env.
SPEECH_KEY = os.getenv('SPEECH_KEY')
SPEECH_REGION = os.getenv('SPEECH_REGION')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
endpoint = os.getenv('endpoint')
key = os.getenv('key')
client = OpenAI(api_key=OPENAI_API_KEY)
global speech_config
speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
locale = ['ja-JP','en-US']
prompt_instance = IntentPrompt()


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



def respondtoUser(text):
    speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesizes the received text to speech.
    # The synthesized speech is expected to be heard on the speaker with this line executed.
    result = speech_synthesizer.speak_text_async(text).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # print("Speech synthesized to speaker for text [{}]".format(text))
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
    return False


def recognize_from_microphone(locale="en-US"):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    # speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

    speech_config.speech_recognition_language = locale  # ja-JP | en-US

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, audio_config=audio_config
    )

    print("Speak into your microphone.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
        return speech_recognition_result.text
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print(
            "No speech could be recognized: {}".format(
                speech_recognition_result.no_match_details
            )
        )
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
    return "NO CONTENT RECOGNIZED"

def userInetraction():

    respondtoUser("Hello! Welcome to Kaizen Cliams - How may I assist you.")
    userCall = recognize_from_microphone(locale[0])
    # st.write("STEP "+str(step) + " : "+userCall)
    # st.write("Strat Intent Extraction.")
    #userIntent = util.prompt_Creation(
    #    userCall, promptLibrary["USER_INTENT_RECOGNITION"], 0.2
    #)
    userIntent = prompt_Creation(
        userCall, prompt_instance.USER_INTENT_PROMPT, 0.1
    )


    ## RESPOND BASED ON CONTEXT
    contextualresponse = prompt_Creation(
        userCall,prompt_instance.EMPATHY, 0.1
    )

    respondtoUser(contextualresponse)


def respondtoUser(text):
    speech_config.speech_synthesis_voice_name = "en-US-AvaMultilingualNeural"

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesizes the received text to speech.
    # The synthesized speech is expected to be heard on the speaker with this line executed.
    result = speech_synthesizer.speak_text_async(text).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # print("Speech synthesized to speaker for text [{}]".format(text))
        return True
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
    return False


def prompt_to_question(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a professional chatbot, given a input convert it to a relevant question.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=50,  # Limit the maximum length of the generated question
        temperature=0.1,  # Controls the randomness of the generated text
        n=1,  # Generate only one response
        stop=None,  # Stop generation at a specific token
    )
    return response.choices[0].message.content


def extractKeyPhrase(key,prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a professional call centre agent, extract only the "+key+" from the text provided: Text "+prompt,
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=50,  # Limit the maximum length of the generated question
        temperature=0.1,  # Controls the randomness of the generated text
        n=1,  # Generate only one response
        stop=None,  # Stop generation at a specific token
    )
    return response.choices[0].message.content