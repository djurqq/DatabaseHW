from fastapi import FastAPI, File, UploadFile, HTTPException, Depends  
from pydantic import BaseModel, validator, Field  
import motor.motor_asyncio  
from bson import ObjectId  # Import ObjectId for MongoDB ID handling
import re  
    
app = FastAPI()  


# Connection string contains username, password and cluster information
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://nikoladurdevicg52857:JKAbgHCQ6bUBP52N@gameassetsdb.0h54gnp.mongodb.net/?retryWrites=true&w=majority&appName=GameAssetsDB")
db = client.gassetsDB  # Connect to the gassetsDB database

# Define data model for player scores using Pydantic with validation
class PlayerScore(BaseModel):
    player_name: str = Field(..., min_length=2, max_length=50)  # Player name field with length constraints
    score: int = Field(..., ge=0)  # Score field (integer) with minimum value of 0
    
    # Validator to ensure player_name doesn't contain potentialy harmful characters
    @validator('player_name')
    def validate_player_name(cls, v):
        # Only allow alphanumeric characters and underscores
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Player name must contain only letters, numbers, and underscores')
        return v

# Custom dependency for validating MongoDB ObjectIds
def validate_object_id(id: str):
    """
    Validates if the provided string is a valid MongoDB ObjectId.
    Returns the ObjectId or raises an HTTPException.
    """
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    return ObjectId(id)
    
# SPRITE ENDPOINTS

# Create a new sprite (POST)
@app.post("/upload_sprite")
async def upload_sprite(file: UploadFile = File(...)):
    """
    Upload a sprite image file to the database.
    The file is stored as binary data in MongoDB.
    """
    # Validate file extension to prevent malicious file uploads
    allowed_extensions = [".png", ".jpg", ".jpeg", ".gif"]
    file_ext = "." + file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed. Only PNG, JPG, JPEG, and GIF are supported.")
    
    # Read the file content as bytes
    content = await file.read()
    
    # Limit file size to 5MB to prevent DoS attacks
    if len(content) > 5 * 1024 * 1024:  # 5MB in bytes
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit")
    
    # Create a dictionary with filename and content
    sprite_doc = {"filename": file.filename, "content": content}
    # Insert the document into the sprites collection
    result = await db.sprites.insert_one(sprite_doc)
    # Return success message with the generated ID
    return {"message": "Sprite uploaded", "id": str(result.inserted_id)}

# Retrieve a sprite by ID (GET)
@app.get("/sprite/{id}")
async def get_sprite(obj_id: ObjectId = Depends(validate_object_id)):
    """
    Retrieve a sprite by its MongoDB ID.
    Returns the sprite document if found.
    """
    try:
        # Query the database for the sprite with the given ID
        # ObjectId is alredy validated by the dependency
        sprite = await db.sprites.find_one({"_id": obj_id})
        
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
async def update_sprite(
    file: UploadFile = File(...),
    obj_id: ObjectId = Depends(validate_object_id)
):
    """
    Update an existing sprite by its MongoDB ID.
    Replaces the old file with a new uploaded file.
    """
    try:
        # Validate file extension to prevent malicious file uploads
        allowed_extensions = [".png", ".jpg", ".jpeg", ".gif"]
        file_ext = "." + file.filename.split(".")[-1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="File type not allowed. Only PNG, JPG, JPEG, and GIF are supported.")
        
        # Read the new file content
        content = await file.read()
        
        # Limit file size to 5MB to prevent DoS attacks
        if len(content) > 5 * 1024 * 1024:  # 5MB in bytes
            raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit")
        
        # Update the sprite document in the database
        result = await db.sprites.update_one(
            {"_id": obj_id},  # Filter by ID
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
async def delete_sprite(obj_id: ObjectId = Depends(validate_object_id)):
    """
    Delete a sprite by its MongoDB ID.
    """
    try:
        # Delete the sprite document from the database
        result = await db.sprites.delete_one({"_id": obj_id})
        
        if result.deleted_count > 0:
            # If sprite was found and deletd
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
    # Validate file extension to prevent malicious file uploads
    allowed_extensions = [".mp3", ".wav", ".ogg", ".flac"]
    file_ext = "." + file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed. Only MP3, WAV, OGG, and FLAC are supported.")
    
    # Read the file content as bytes
    content = await file.read()
    
    # Limit file size to 10MB to prevent DoS attacks
    if len(content) > 10 * 1024 * 1024:  # 10MB in bytes
        raise HTTPException(status_code=400, detail="File size exceeds the 10MB limit")
    
    # Create a dictionary with filename and content
    audio_doc = {"filename": file.filename, "content": content}
    # Insert the document into the audio collection
    result = await db.audio.insert_one(audio_doc)
    # Return success message with the generated ID
    return {"message": "Audio file uploaded", "id": str(result.inserted_id)}

# Retrieve an audio file by ID (GET)
@app.get("/audio/{id}")
async def get_audio(obj_id: ObjectId = Depends(validate_object_id)):
    """
    Retrieve an audio file by its MongoDB ID.
    Returns the audio document if found.
    """
    try:
        # Query the database for the audio file with the given ID
        audio = await db.audio.find_one({"_id": obj_id})
        
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
async def update_audio(
    file: UploadFile = File(...),
    obj_id: ObjectId = Depends(validate_object_id)
):
    """
    Update an existing audio file by its MongoDB ID.
    Replaces the old file with a new uploaded file.
    """
    try:
        # Validate file extension to prevent malicious file uploads
        allowed_extensions = [".mp3", ".wav", ".ogg", ".flac"]
        file_ext = "." + file.filename.split(".")[-1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(status_code=400, detail="File type not allowed. Only MP3, WAV, OGG, and FLAC are supported.")
        
        # Read the new file content
        content = await file.read()
        
        # Limit file size to 10MB to prevent DoS attacks
        if len(content) > 10 * 1024 * 1024:  # 10MB in bytes
            raise HTTPException(status_code=400, detail="File size exceeds the 10MB limit")
        
        # Update the audio document in the database
        result = await db.audio.update_one(
            {"_id": obj_id},  # Filter by ID
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
async def delete_audio(obj_id: ObjectId = Depends(validate_object_id)):
    """
    Delete an audio file by its MongoDB ID.
    """
    try:
        # Delete the audio document from the database
        result = await db.audio.delete_one({"_id": obj_id})
        
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
    # Pydantic model already validates the data
    # Convert the Pydantic model to a dictionary
    score_doc = score.dict()
    
    # Check if a player with this name already exists to prevent duplicates
    existing_player = await db.scores.find_one({"player_name": score.player_name})
    if existing_player:
        raise HTTPException(status_code=400, detail="A player with this name already exists")
    
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
        # Validate player name format
        if not re.match(r'^[a-zA-Z0-9_]+$', player_name):
            raise HTTPException(status_code=400, detail="Invalid player name format")
        
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
        # Validate player name format
        if not re.match(r'^[a-zA-Z0-9_]+$', player_name):
            raise HTTPException(status_code=400, detail="Invalid player name format")
        
        # Ensure the URL player_name matches the JSON body player_name
        if player_name != score.player_name:
            raise HTTPException(status_code=400, detail="Player name in URL does not match player name in request body")
        
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
        # Validate player name format
        if not re.match(r'^[a-zA-Z0-9_]+$', player_name):
            raise HTTPException(status_code=400, detail="Invalid player name format")
        
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