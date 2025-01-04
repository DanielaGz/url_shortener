from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from schemas import URLCreate, URLResponse
from datetime import datetime
from database import connectDb
from dotenv import load_dotenv
import random
import string
import os


load_dotenv()

CURRENT_URL = os.getenv("CURRENT_URL")

app = FastAPI()


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
