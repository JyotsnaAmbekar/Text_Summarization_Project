#!/usr/bin/env python3
import sys
import os
sys.path.append('src')

from fastapi import FastAPI
import uvicorn
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from fastapi.responses import Response
from textSummarizer.pipeline.prediction import PredictionPipeline


text = "What is Text Summarization?"

app = FastAPI()

@app.get("/", tags=["authentication"])
def index():
    return RedirectResponse(url="/docs")



@app.get("/train")
def training():
    try:
        os.system("python main.py")
        return Response("Training successful !!")

    except Exception as e:
        return Response("Error Occurred! {}".format(e))
    



@app.post("/predict")
def predict_route(text):
    try:

        obj = PredictionPipeline()
        text = obj.predict(text)
        return text
    except Exception as e:
        raise e
    

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)