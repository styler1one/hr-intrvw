"""
Templates API endpoint
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from templates import get_all_templates

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/templates")
async def get_templates():
    """Get all available interview templates"""
    return {
        "templates": get_all_templates()
    }
