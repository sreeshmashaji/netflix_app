import React, { useEffect, useState } from 'react'
import './Banner.css'
import '../../App.css'

import axios from 'axios'

function Banner() {

    const [movie, setMovie] = useState('')

    useEffect(() => {
        axios.get("http://localhost:8000/movies/movies_by_genre/66dfe9f0ba6e7fad97b37cba")
            .then((res) => {
                console.log(res.data)
                const movies = res.data.data; // assuming 'data' is an array of movies
                if (movies.length > 0) {
                    // Generate a random index based on the length of the movies array
                    const randomIndex = Math.floor(Math.random() * movies.length);
                    setMovie(movies[randomIndex]); // Set the movie based on the random index
                }
            })
            .catch((err) => {
                console.error("Error fetching movie:", err);
            });
    }, [])

    return (
        <div 
            className='banner' 
            style={{ backgroundImage: `url(${movie ? movie.banner_image : " "})` }} // Correct inline style for background image
        >
            <div className='content'>
                <h1 className='title'>{movie ? movie.title : ""}</h1>
                <div className='banner_buttons'>
                    <button className='button'>Play</button>
                    <button className='button'>My List</button>
                </div>

                <h1 className='description'>{movie ? movie.overview : " "}</h1>
            </div>
            <div className='fade'></div>
        </div>
    )
}

export default Banner
