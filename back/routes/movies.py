from bson import ObjectId
from fastapi import APIRouter, HTTPException, File, UploadFile, Form, status
from typing import List, Optional
from datetime import datetime
import os
import shutil
from pathlib import Path
from database import db

router = APIRouter(prefix="/movies", tags=["movies"])

# Directory to store images
IMAGE_DIR = Path("images")
IMAGE_DIR.mkdir(parents=True, exist_ok=True)  # Create directory if it doesn't exist

collection = db.movies

@router.post('', summary="Add a movie")
async def add_movie(
    title: str = Form(...),
    overview: str = Form(...),
    media_type: str = Form(...),
    adult: bool = Form(...),
    original_language: str = Form(...),
    popularity: float = Form(...),
    release_date: Optional[str] = Form(None),
    first_air_date: Optional[str] = Form(None),
    vote_average: float = Form(...),
    vote_count: int = Form(...),
    origin_country: Optional[List[str]] = Form(None),
    genre_ids: List[str] = Form(...),  # Include genre IDs
    movie_image: UploadFile = File(None)  # Handling the movie image upload
):
    try:
        # Handle movie image
        image_url = None
        if movie_image:
            allowed_extensions = ['png', 'jpg', 'jpeg']
            file_ext = movie_image.filename.split('.')[-1]
            if file_ext.lower() not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PNG, JPG, and JPEG formats are allowed for the image"
                )

            file_location = os.path.join(IMAGE_DIR, movie_image.filename)
            try:
                with open(file_location, "wb") as buffer:
                    shutil.copyfileobj(movie_image.file, buffer)
                image_url = f"http://localhost:8000/images/{movie_image.filename}"
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to save image: {str(e)}"
                )

        # Prepare data for insertion
        data = {
            'title': title,
            'overview': overview,
            'media_type': media_type,
            'adult': adult,
            'original_language': original_language,
            'popularity': popularity,
            'release_date': release_date,
            'first_air_date': first_air_date,
            'vote_average': vote_average,
            'vote_count': vote_count,
            'origin_country': origin_country,
            'genre_ids': genre_ids,  # Include genre IDs
            'image': image_url,
            'date_added': datetime.now()
        }

        # Insert movie into database
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

@router.put('/update/{movie_id}', summary="Update a movie")
async def update_movie(
    movie_id: str,
    title: Optional[str] = Form(None),
    overview: Optional[str] = Form(None),
    media_type: Optional[str] = Form(None),
    adult: Optional[bool] = Form(None),
    original_language: Optional[str] = Form(None),
    popularity: Optional[float] = Form(None),
    release_date: Optional[str] = Form(None),
    first_air_date: Optional[str] = Form(None),
    vote_average: Optional[float] = Form(None),
    vote_count: Optional[int] = Form(None),
    origin_country: Optional[List[str]] = Form(None),
    genre_ids: Optional[List[str]] = Form(None),  # Include genre IDs
    movie_image: Optional[UploadFile] = File(None)  # Handling the movie image upload
):
    try:
        # Find the movie by ID
        movie = collection.find_one({'_id': ObjectId(movie_id)})
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )

        update_data = {}
        if title:
            update_data['title'] = title
        if overview:
            update_data['overview'] = overview
        if media_type:
            update_data['media_type'] = media_type
        if adult is not None:
            update_data['adult'] = adult
        if original_language:
            update_data['original_language'] = original_language
        if popularity:
            update_data['popularity'] = popularity
        if release_date:
            update_data['release_date'] = release_date
        if first_air_date:
            update_data['first_air_date'] = first_air_date
        if vote_average:
            update_data['vote_average'] = vote_average
        if vote_count:
            update_data['vote_count'] = vote_count
        if origin_country:
            update_data['origin_country'] = origin_country
        if genre_ids is not None:
            update_data['genre_ids'] = genre_ids  # Update genre IDs
        if movie_image:
            allowed_extensions = ['png', 'jpg', 'jpeg']
            file_ext = movie_image.filename.split('.')[-1]
            if file_ext.lower() not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PNG, JPG, and JPEG formats are allowed for the image"
                )

            file_location = os.path.join(IMAGE_DIR, movie_image.filename)
            try:
                with open(file_location, "wb") as buffer:
                    shutil.copyfileobj(movie_image.file, buffer)
                update_data['image'] = f"http://localhost:8000/images/{movie_image.filename}"
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to save image: {str(e)}"
                )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No update data provided"
            )

        collection.update_one({'_id': ObjectId(movie_id)}, {'$set': update_data})

        updated_movie = collection.find_one({'_id': ObjectId(movie_id)})
        updated_movie["_id"] = str(updated_movie["_id"])

        return {"message": "success", "data": updated_movie}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.delete('/delete/{movie_id}', summary="Delete a movie")
async def delete_movie(movie_id: str):
    try:
        result = collection.delete_one({'_id': ObjectId(movie_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )

        return {"message": "success", "detail": "Movie deleted"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get('/{movie_id}', summary="Get a movie")
async def get_movie(movie_id: str):
    try:
        movie = collection.find_one({'_id': ObjectId(movie_id)})
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found"
            )

        movie["_id"] = str(movie["_id"])
        return {"message": "success", "data": movie}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get('', summary="Get all movies")
async def get_all_movies():
    try:
        movies = list(collection.find())
        for movie in movies:
            movie["_id"] = str(movie["_id"])
        return {"message": "success", "data": movies}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )