from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.schemas.request import CareerQuery
from app.agents.career_agent import run_career_agent
from app.routes.career_routes import router as career_router  # ✅ Add this import

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# UI + Template setup
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ✅ Include the career router
app.include_router(career_router)

# Existing API endpoints
@app.get("/status")
def root():
    return {"message": "AI Career Agent is running"}

@app.post("/suggest")
def suggest_career(query: CareerQuery):
    result = run_career_agent(query.interests)
    return result
