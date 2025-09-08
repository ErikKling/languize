from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from app.api.routes import router

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

print("DEBUG: Registered routes:")
for route in app.routes:
    print(f"Name: {getattr(route, 'name', None)}, Path: {getattr(route, 'path', None)}")

app.include_router(router)

@app.get("/")
def hello():
    return {"message": "Hello from FastAPI!"}

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.get("/learn", response_class=HTMLResponse)
async def learn_view(request: Request):
    return templates.TemplateResponse("learn.html", {"request": request})