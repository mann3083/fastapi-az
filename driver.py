from fastapi import FastAPI,Body

app = FastAPI()


@app.get("/")
def simpleGet():
    return {"message":"Welcome to Azure"}

@app.post("/insert")
def simplepost(newD = Body()):
    newD['someKey'] = "there is no data validation"
    return newD
