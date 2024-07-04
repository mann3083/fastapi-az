from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import azure.cognitiveservices.speech as speechsdk
import os,logging
import util,json
from dotenv import load_dotenv


logging.basicConfig(level=logging.INFO)
load_dotenv()

#SPEECH_KEY = os.getenv("SPEECH_KEY")
#SPEECH_REGION = os.getenv("SPEECH_REGION")


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def get(request: Request):
    logging.info("LANIDNG PAGE")
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload-audio/")
def upload_audio(file: UploadFile = File(...)):
    logging.info("UPLOAD AUDIO PAGE")
    try:
        # Save the uploaded file to a temporary location
        audio_file_location = os.path.join("temp", file.filename)
        input_file = "/temp/audio.webm"
        output_file = "/temp/audio.wav"
        logging.info("CONVERT FILE")
        util.convert_webm_to_wav(input_file, output_file)


        ###  TO BE IMPLEMENTED


        """ logging.info("UPLOAD AUDIO "+str(audio_file_location))
        # Convert speech to text
        text = util.convert_speech_to_text(audio_file_location)

        # Convert text to speech - WORKING
        #speech_file = util.convert_text_to_speech(text) """

        return {"text": text}

    except Exception as e:
        #raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        return {"audioFileLocation": audio_file_location}




@app.post("/upload-audio-arch/")
async def upload_audio(file: UploadFile = File(...)):

    try:
        # Save the uploaded file
        file_location = f"temp/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        # Configure Azure Speech SDK
        speech_config = speechsdk.SpeechConfig(
            subscription=SPEECH_KEY, region=SPEECH_REGION
        )
        audio_config = speechsdk.audio.AudioConfig(filename=file_location)
        recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, audio_config=audio_config
        )

        # Recognize speech
        result = recognizer.recognize_once()

        # Remove the temporary file
        os.remove(file_location)

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return {"text": result.text}
        else:
            return {"error": result.reason}
    except Exception as e:
        # raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
        exception_message = str(e)
        print(exception_message)


# Run the app with: uvicorn fullstack:app --reload
