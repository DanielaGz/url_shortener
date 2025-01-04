from motor.motor_asyncio import AsyncIOMotorClient
import os

async def connectDb(app):
    app.mongodb_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
    app.mongodb = app.mongodb_client["shortener_project"] 
    collection = app.mongodb["temporalData"]
    await collection.create_index([("createdAt", 1)], expireAfterSeconds=86400)