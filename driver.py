from fastapi import FastAPI,Body
import util

app = FastAPI()


@app.get("/")
def simpleGet():
    return {"message":"Welcome to Azure Region "+util.SPEECH_REGION}

@app.post("/insert")
def simplepost(newD = Body()):
    newD['someKey'] = "there is no data validation"
    return newD
