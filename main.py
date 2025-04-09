from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio
from bson import ObjectId
    
app = FastAPI()

# Connect to Mongo Atlas
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://nikoladurdevicg52857:JKAbgHCQ6bUBP52N@gameassetsdb.0h54gnp.mongodb.net/?retryWrites=true&w=majority&appName=GameAssetsDB")
db = client.gassetsDB

class PlayerScore(BaseModel):
    player_name: str
    score: int
    
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    # In a real application, the file should be saved to a storage service
    content = await file.read()
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.get("/sprite/{id}")
async def get_sprite(id: str):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        sprite = await db.sprites.find_one({"_id": ObjectId(id)})
        if sprite:
            sprite["_id"] = str(sprite["_id"])  # Convert ObjectId to string
            return sprite
        else:
            raise HTTPException(status_code=404, detail="Sprite not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving sprite: {str(e)}")

@app.put("/sprite/{id}")
async def update_sprite(id: str, file: UploadFile = File(...)):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        content = await file.read()
        result = await db.sprites.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"content": content, "filename": file.filename}}
        )
        if result.matched_count > 0:
            return {"message": "Sprite updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Sprite not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating sprite: {str(e)}")

@app.delete("/sprite/{id}")
async def delete_sprite(id: str):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        result = await db.sprites.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return {"message": "Sprite deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Sprite not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting sprite: {str(e)}")

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

@app.get("/audio/{id}")
async def get_audio(id: str):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        audio = await db.audio.find_one({"_id": ObjectId(id)})
        if audio:
            audio["_id"] = str(audio["_id"])  # Convert ObjectId to string
            return audio
        else:
            raise HTTPException(status_code=404, detail="Audio not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving audio: {str(e)}")

@app.put("/audio/{id}")
async def update_audio(id: str, file: UploadFile = File(...)):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        content = await file.read()
        result = await db.audio.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"content": content, "filename": file.filename}}
        )
        if result.matched_count > 0:
            return {"message": "Audio updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Audio not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating audio: {str(e)}")

@app.delete("/audio/{id}")
async def delete_audio(id: str):
    try:
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        result = await db.audio.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return {"message": "Audio deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Audio not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting audio: {str(e)}")

@app.post("/player_score")
async def add_score(score: PlayerScore):
    score_doc = score.dict()
    result = await db.scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}

@app.get("/player_score/{player_name}")
async def get_player_score(player_name: str):
    try:
        score = await db.scores.find_one({"player_name": player_name})
        if score:
            score["_id"] = str(score["_id"])  # Convert ObjectId to string
            return score
        else:
            raise HTTPException(status_code=404, detail="Player score not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving player score: {str(e)}")

@app.put("/player_score/{player_name}")
async def update_player_score(player_name: str, score: PlayerScore):
    try:
        result = await db.scores.update_one(
            {"player_name": player_name},
            {"$set": {"score": score.score}}
        )
        if result.matched_count > 0:
            return {"message": "Player score updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Player score not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating player score: {str(e)}")

@app.delete("/player_score/{player_name}")
async def delete_player_score(player_name: str):
    try:
        result = await db.scores.delete_one({"player_name": player_name})
        if result.deleted_count > 0:
            return {"message": "Player score deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Player score not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting player score: {str(e)}")