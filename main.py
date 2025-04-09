from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio
    
app = FastAPI()

# Connect to Mongo Atlas
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://nikoladurdevicg52857:JKAbgHCQ6bUBP52N@gameassetsdb.0h54gnp.mongodb.net/?retryWrites=true&w=majority&appName=GameAssetsDB")
db = client.gassetsDB

class PlayerScore(BaseModel):
    player_name: str
    score: int
    
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    content = await file.read()
    sprite_doc = {"filename": file.filename, "content": content}
    result = await db.sprites.insert_one(sprite_doc)
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

@app.get("/upload_sprite/{filename}")
async def get_sprite(filename: str):
    sprite = await db.sprites.find_one({"filename": filename})
    if not sprite:
        raise HTTPException(status_code=404, detail="Sprite not found")
    sprite["_id"] = str(sprite["_id"])  # Convert ObjectId to string
    return sprite

@app.put("/upload_sprite/{filename}")
async def update_sprite(filename: str, file: UploadFile = File(...)):
    content = await file.read()
    result = await db.sprites.update_one(
        {"filename": filename},
        {"$set": {"content": content}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return {"message": "Sprite updated"}

@app.delete("/upload_sprite/{filename}")
async def delete_sprite(filename: str):
    result = await db.sprites.delete_one({"filename": filename})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sprite not found")
    return {"message": "Sprite deleted"}

@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    content = await file.read()
    audio_doc = {"filename": file.filename, "content": content}
    result = await db.audio.insert_one(audio_doc)
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

@app.get("/upload_audio/{filename}")
async def get_audio(filename: str):
    audio = await db.audio.find_one({"filename": filename})
    if not audio:
        raise HTTPException(status_code=404, detail="Audio file not found")
    audio["_id"] = str(audio["_id"])  # Convert ObjectId to string
    return audio

@app.put("/upload_audio/{filename}")
async def update_audio(filename: str, file: UploadFile = File(...)):
    content = await file.read()
    result = await db.audio.update_one(
        {"filename": filename},
        {"$set": {"content": content}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return {"message": "Audio file updated"}

@app.delete("/upload_audio/{filename}")
async def delete_audio(filename: str):
    result = await db.audio.delete_one({"filename": filename})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Audio file not found")
    return {"message": "Audio file deleted"}

@app.post("/player_score")
async def add_score(score: PlayerScore):
    score_doc = score.dict()
    result = await db.scores.insert_one(score_doc)
    return {"message": "Score recorded", "id": str(result.inserted_id)}

@app.get("/player_score/{player_name}")
async def get_player_score(player_name: str):
    score = await db.scores.find_one({"player_name": player_name})
    if not score:
        raise HTTPException(status_code=404, detail="Player not found")
    score["_id"] = str(score["_id"])  # Convert ObjectId to string
    return score

@app.put("/player_score/{player_name}")
async def update_player_score(player_name: str, updated_score: PlayerScore):
    result = await db.scores.update_one(
        {"player_name": player_name},
        {"$set": updated_score.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": "Player score updated"}

@app.delete("/player_score/{player_name}")
async def delete_player_score(player_name: str):
    result = await db.scores.delete_one({"player_name": player_name})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Player not found")
    return {"message": "Player score deleted"}