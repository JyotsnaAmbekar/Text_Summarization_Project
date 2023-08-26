from fastapi import FastAPI, Form, Request
import uvicorn
import sys
import os
sys.path.append('src')
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse, HTMLResponse
from fastapi.responses import Response
from textSummarizer.pipeline.prediction import PredictionPipeline

text:str = "Text Summarization"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "text": "", "summarized_text": ""})

@app.get("/train")
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

@app.post("/predict", response_class=HTMLResponse)
async def predict_route(request: Request, text: str = Form(...)):
    try:
        # Debug: Check if the function is being called
        print("predict_route function called")

        obj = PredictionPipeline()
        summarized_text = obj.predict(text)

        # Debug: Check the summarized_text before rendering the template
        print("Summarized Text:", summarized_text)

        return templates.TemplateResponse(
            "index.html",
            {"request": request, "text": text, "summarized_text": summarized_text}
        )
    except Exception as e:
        raise e


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)

