from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from schemas import URLCreate, URLResponse
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from database import connectDb
from dotenv import load_dotenv
import random
import string
import os


load_dotenv()

CURRENT_URL = os.getenv("CURRENT_URL")

# Accede a las variables de entorno
current_url = os.getenv("CURRENT_URL")
mongo_uri = os.getenv("MONGO_URI")

# Usa las variables como lo necesites
print(f"Current URL: {current_url}")
print(f"Mongo URI: {mongo_uri}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db():
    await connectDb(app)


@app.on_event("shutdown")
async def shutdown_db():
    app.mongodb_client.close()


def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


@app.post(
    "/shorten",
    response_model=URLResponse,
    summary="Generate shortened link"
)
async def shorten_url(url: URLCreate):
    collection = app.mongodb["temporalData"]

    short_id = generate_short_id()

    doc = {
        "short_url": f"{CURRENT_URL}/{short_id}",
        "long_url": str(url.long_url),
        "createdAt": datetime.utcnow()
    }

    await collection.insert_one(doc)

    return {
        "short_url": f"{CURRENT_URL}/{short_id}",
        "long_url": str(url.long_url)
    }


@app.get("/{short_id}", summary="Redirect from a shortened link")
async def redirect_to_url(short_id: str):
    collection = app.mongodb["temporalData"]
    temp_url = await collection.find_one({"short_url": f"{CURRENT_URL}/{short_id}"})

    if temp_url:
        return RedirectResponse(url=temp_url["long_url"])

    raise HTTPException(status_code=404, detail="URL not found")
