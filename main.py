from fastapi import FastAPI, File, UploadFile, HTTPException  # Import FastAPI framework and related utilities
from pydantic import BaseModel  # Import BaseModel for request body validation
import motor.motor_asyncio  # Import MongoDB async driver
from bson import ObjectId  # Import ObjectId for MongoDB ID handling
    
app = FastAPI()  # Initialize the FastAPI application

# Connect to MongoDB Atlas cloud database
# Connection string contains username, password and cluster information
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://nikoladurdevicg52857:JKAbgHCQ6bUBP52N@gameassetsdb.0h54gnp.mongodb.net/?retryWrites=true&w=majority&appName=GameAssetsDB")
db = client.gassetsDB  # Connect to the gassetsDB database

# Define data model for player scores using Pydantic
class PlayerScore(BaseModel):
    player_name: str  # Player name field
    score: int  # Score field (integer)
    
# SPRITE ENDPOINTS

# Create a new sprite (POST)
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    """
    Upload a sprite image file to the database.
    The file is stored as binary data in MongoDB.
    """
    # Read the file content as bytes
    content = await file.read()
    # Create a dictionary with filename and content
    sprite_doc = {"filename": file.filename, "content": content}
    # Insert the document into the sprites collection
    result = await db.sprites.insert_one(sprite_doc)
    # Return success message with the generated ID
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

# Retrieve a sprite by ID (GET)
@app.get("/sprite/{id}")
async def get_sprite(id: str):
    """
    Retrieve a sprite by its MongoDB ID.
    Returns the sprite document if found.
    """
    try:
        # Validate if the provided ID is a valid MongoDB ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Query the database for the sprite with the given ID
        sprite = await db.sprites.find_one({"_id": ObjectId(id)})
        
        if sprite:
            # Convert the ObjectId to string for JSON serialization
            sprite["_id"] = str(sprite["_id"])
            return sprite
        else:
            # If sprite not found, return 404 error
            raise HTTPException(status_code=404, detail="Sprite not found")
    except Exception as e:
        # Catch any other errors and return 500 error
        raise HTTPException(status_code=500, detail=f"Error retrieving sprite: {str(e)}")

# Update a sprite by ID (PUT)
@app.put("/sprite/{id}")
async def update_sprite(id: str, file: UploadFile = File(...)):
    """
    Update an existing sprite by its MongoDB ID.
    Replaces the old file with a new uploaded file.
    """
    try:
        # Validate if the provided ID is a valid MongoDB ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Read the new file content
        content = await file.read()
        
        # Update the sprite document in the database
        result = await db.sprites.update_one(
            {"_id": ObjectId(id)},  # Filter by ID
            {"$set": {"content": content, "filename": file.filename}}  # Update content and filename
        )
        
        if result.matched_count > 0:
            # If sprite was found and updated
            return {"message": "Sprite updated successfully"}
        else:
            # If no sprite with that ID exists
            raise HTTPException(status_code=404, detail="Sprite not found")
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=f"Error updating sprite: {str(e)}")

# Delete a sprite by ID (DELETE)
@app.delete("/sprite/{id}")
async def delete_sprite(id: str):
    """
    Delete a sprite by its MongoDB ID.
    """
    try:
        # Validate if the provided ID is a valid MongoDB ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Delete the sprite document from the database
        result = await db.sprites.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count > 0:
            # If sprite was found and deleted
            return {"message": "Sprite deleted successfully"}
        else:
            # If no sprite with that ID exists
            raise HTTPException(status_code=404, detail="Sprite not found")
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=f"Error deleting sprite: {str(e)}")

# AUDIO ENDPOINTS

# Create a new audio file (POST)
@app.post("/upload_audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload an audio file to the database.
    The file is stored as binary data in MongoDB.
    """
    # Read the file content as bytes
    content = await file.read()
    # Create a dictionary with filename and content
    audio_doc = {"filename": file.filename, "content": content}
    # Insert the document into the audio collection
    result = await db.audio.insert_one(audio_doc)
    # Return success message with the generated ID
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

# Retrieve an audio file by ID (GET)
@app.get("/audio/{id}")
async def get_audio(id: str):
    """
    Retrieve an audio file by its MongoDB ID.
    Returns the audio document if found.
    """
    try:
        # Validate if the provided ID is a valid MongoDB ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Query the database for the audio file with the given ID
        audio = await db.audio.find_one({"_id": ObjectId(id)})
        
        if audio:
            # Convert the ObjectId to string for JSON serialization
            audio["_id"] = str(audio["_id"])
            return audio
        else:
            # If audio file not found, return 404 error
            raise HTTPException(status_code=404, detail="Audio not found")
    except Exception as e:
        # Catch any other errors and return 500 error
        raise HTTPException(status_code=500, detail=f"Error retrieving audio: {str(e)}")

# Update an audio file by ID (PUT)
@app.put("/audio/{id}")
async def update_audio(id: str, file: UploadFile = File(...)):
    """
    Update an existing audio file by its MongoDB ID.
    Replaces the old file with a new uploaded file.
    """
    try:
        # Validate if the provided ID is a valid MongoDB ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Read the new file content
        content = await file.read()
        
        # Update the audio document in the database
        result = await db.audio.update_one(
            {"_id": ObjectId(id)},  # Filter by ID
            {"$set": {"content": content, "filename": file.filename}}  # Update content and filename
        )
        
        if result.matched_count > 0:
            # If audio file was found and updated
            return {"message": "Audio updated successfully"}
        else:
            # If no audio file with that ID exists
            raise HTTPException(status_code=404, detail="Audio not found")
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=f"Error updating audio: {str(e)}")

# Delete an audio file by ID (DELETE)
@app.delete("/audio/{id}")
async def delete_audio(id: str):
    """
    Delete an audio file by its MongoDB ID.
    """
    try:
        # Validate if the provided ID is a valid MongoDB ObjectId
        if not ObjectId.is_valid(id):
            raise HTTPException(status_code=400, detail="Invalid ID format")
        
        # Delete the audio document from the database
        result = await db.audio.delete_one({"_id": ObjectId(id)})
        
        if result.deleted_count > 0:
            # If audio file was found and deleted
            return {"message": "Audio deleted successfully"}
        else:
            # If no audio file with that ID exists
            raise HTTPException(status_code=404, detail="Audio not found")
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=f"Error deleting audio: {str(e)}")

# PLAYER SCORE ENDPOINTS

# Create a new player score (POST)
@app.post("/player_score")
async def add_score(score: PlayerScore):
    """
    Add a new player score to the database.
    The score object contains player_name and score value.
    """
    # Convert the Pydantic model to a dictionary
    score_doc = score.dict()
    # Insert the score document into the scores collection
    result = await db.scores.insert_one(score_doc)
    # Return success message with the generated ID
    return {"message": "Score recorded", "id": str(result.inserted_id)}

# Retrieve a player score by player name (GET)
@app.get("/player_score/{player_name}")
async def get_player_score(player_name: str):
    """
    Retrieve a player's score by their name.
    Returns the score document if found.
    """
    try:
        # Query the database for the score with the given player name
        score = await db.scores.find_one({"player_name": player_name})
        
        if score:
            # Convert the ObjectId to string for JSON serialization
            score["_id"] = str(score["_id"])
            return score
        else:
            # If player score not found, return 404 error
            raise HTTPException(status_code=404, detail="Player score not found")
    except Exception as e:
        # Catch any other errors and return 500 error
        raise HTTPException(status_code=500, detail=f"Error retrieving player score: {str(e)}")

# Update a player score by player name (PUT)
@app.put("/player_score/{player_name}")
async def update_player_score(player_name: str, score: PlayerScore):
    """
    Update an existing player's score by their name.
    """
    try:
        # Update the score document in the database
        result = await db.scores.update_one(
            {"player_name": player_name},  # Filter by player name
            {"$set": {"score": score.score}}  # Update only the score value
        )
        
        if result.matched_count > 0:
            # If player score was found and updated
            return {"message": "Player score updated successfully"}
        else:
            # If no player score with that name exists
            raise HTTPException(status_code=404, detail="Player score not found")
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=f"Error updating player score: {str(e)}")

# Delete a player score by player name (DELETE)
@app.delete("/player_score/{player_name}")
async def delete_player_score(player_name: str):
    """
    Delete a player's score by their name.
    """
    try:
        # Delete the score document from the database
        result = await db.scores.delete_one({"player_name": player_name})
        
        if result.deleted_count > 0:
            # If player score was found and deleted
            return {"message": "Player score deleted successfully"}
        else:
            # If no player score with that name exists
            raise HTTPException(status_code=404, detail="Player score not found")
    except Exception as e:
        # Catch any other errors
        raise HTTPException(status_code=500, detail=f"Error deleting player score: {str(e)}")