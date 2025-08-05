from app.api.routes import router
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
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
