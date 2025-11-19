"""
Main API entry point for Vercel deployment
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Volentis Interview Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Volentis Interview Agent API",
        "version": "1.0.0-vercel",
        "status": "running"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}
