from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import upload, chat
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="SmartDoc API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "SmartDoc API is running"}