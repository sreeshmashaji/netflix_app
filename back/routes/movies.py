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
    adult: Optional[bool] = Form(None),
    
    genre_ids: List[str] = Form(...),  # Include genre IDs
    movie_image: UploadFile = File(None) , # Handling the movie image upload
    banner_image:UploadFile=File(None)
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


        banner=None
        if banner_image:
            allowed_extensions = ['png', 'jpg', 'jpeg']
            file_ext = banner_image.filename.split('.')[-1]
            if file_ext.lower() not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PNG, JPG, and JPEG formats are allowed for the image"
                )

            file_location = os.path.join(IMAGE_DIR, banner_image.filename)
            try:
                with open(file_location, "wb") as buffer:
                    shutil.copyfileobj(banner_image.file, buffer)
                banner = f"http://localhost:8000/images/{banner_image.filename}"
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
            'adult': True,
           
            'genre_ids': genre_ids,  # Include genre IDs
            'image': image_url,
            'banner_image':banner,
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
   
    genre_ids: Optional[List[str]] = Form(None),  # Include genre IDs
    movie_image: Optional[UploadFile] = File(None) , # Handling the movie image upload
    banner_image:Optional[UploadFile]=File(None)
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
        
        if banner_image:
            allowed_extensions = ['png', 'jpg', 'jpeg']
            file_ext = banner_image.filename.split('.')[-1]
            if file_ext.lower() not in allowed_extensions:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only PNG, JPG, and JPEG formats are allowed for the image"
                )

            file_location = os.path.join(IMAGE_DIR, banner_image.filename)
            try:
                with open(file_location, "wb") as buffer:
                    shutil.copyfileobj(banner_image.file, buffer)
                update_data["banner_image"] = f"http://localhost:8000/images/{banner_image.filename}"
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Failed to save image: {str(e)}"
                )




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
    




@router.get('/movies_by_genre/{genre_id}', summary="Get restaurants based on a single genre ID")
async def get_restaurants_by_genre(genre_id: str):
    try:
        # Find movies that match the genre_id
        matched_movies = collection.find({'genre_ids': genre_id})
        
        
        restaurant_list = []
        for restaurant in matched_movies:
            restaurant["_id"] = str(restaurant["_id"])
            restaurant_list.append(restaurant)

        if not restaurant_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No restaurants found for the provided genre"
            )

        return {"message": "success", "data": restaurant_list}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )