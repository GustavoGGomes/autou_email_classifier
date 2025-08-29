from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import io

from .model import classify, suggest_reply
from .nlp import preprocess

import PyPDF2

app = FastAPI(title="AutoU – Email Classifier")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

def read_pdf(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text = []
        for page in reader.pages:
            text.append(page.extract_text() or "")
        return "\n".join(text).strip()
    except Exception:
        return ""

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/process", response_class=HTMLResponse)
async def process(request: Request, email_text: Optional[str] = Form(None), file: Optional[UploadFile] = File(None)):
    content = (email_text or "").strip()
    filename = None

    if (not content) and file is not None:
        filename = file.filename
        data = await file.read()
        if filename.lower().endswith(".pdf"):
            content = read_pdf(data)
        elif filename.lower().endswith(".txt"):
            content = data.decode("utf-8", errors="ignore")
        else:
            content = ""

    if not content:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Forneça um .txt/.pdf ou cole o texto do email.", "result": None})

    clf = classify(content)
    reply = suggest_reply(content, clf["label"])
    return templates.TemplateResponse("index.html", {"request": request, "result": {"input": content, "analysis": clf, "reply": reply}, "filename": filename})