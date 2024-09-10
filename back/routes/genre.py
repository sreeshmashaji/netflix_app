from fastapi import APIRouter, HTTPException, Form, status
from typing import List, Optional
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/genres", tags=["genres"])

# Assuming a database connection is already established in your code
from database import db

collection = db.genres

@router.post('/', summary="Create a genre")
async def create_genre(
    name: str = Form(...)
):
    try:
        # Prepare data for insertion
        data = {
            'name': name,
            'date_added': datetime.now()
        }

        # Insert genre into database
        inserted_data = collection.insert_one(data)

        result_data = collection.find_one({'_id': inserted_data.inserted_id})
        result_data["_id"] = str(result_data["_id"])

        if not result_data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sorry, operation failed"
            )

        return {"message": "success", "data": result_data}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.put('/update/{genre_id}', summary="Update a genre")
async def update_genre(
    genre_id: str,
    name: Optional[str] = Form(None)
):
    try:
        # Find the genre by ID
        genre = collection.find_one({'_id': ObjectId(genre_id)})
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre not found"
            )

        update_data = {}
        if name:
            update_data['name'] = name

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided"
            )

        collection.update_one({'_id': ObjectId(genre_id)}, {'$set': update_data})

        updated_genre = collection.find_one({'_id': ObjectId(genre_id)})
        updated_genre["_id"] = str(updated_genre["_id"])

        return {"message": "success", "data": updated_genre}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete('/delete/{genre_id}', summary="Delete a genre")
async def delete_genre(genre_id: str):
    try:
        result = collection.delete_one({'_id': ObjectId(genre_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre not found"
            )

        return {"message": "success", "detail": "Genre deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get('/{genre_id}', summary="Get a genre")
async def get_genre(genre_id: str):
    try:
        genre = collection.find_one({'_id': ObjectId(genre_id)})
        if not genre:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Genre not found"
            )

        genre["_id"] = str(genre["_id"])
        return {"message": "success", "data": genre}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get('/', summary="Get all genres")
async def get_all_genres():
    try:
        genres = list(collection.find())
        for genre in genres:
            genre["_id"] = str(genre["_id"])
        return {"message": "success", "data": genres}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
