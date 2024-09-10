import React ,{useEffect,useState} from 'react'
import './RowPoster.css'
import axios from 'axios'


function RowPoster() {

  const [movies, setMovies] = useState([])
  useEffect(() => {

    axios.get("http://localhost:8000/movies/movies_by_genre/66dfe9f0ba6e7fad97b37cba")
    .then((res) => {
        console.log(res.data)
        console.log("res", res.data.data)
        setMovies(res.data.data)
    })
    .catch((err) => {
        console.error("Error fetching movie:", err);
    });
   
  }, [])
  
  return (
    <div className='row'>
        
        <h2>Title</h2>
        <div className='posters'>
        {movies.map((movie)=>{
          return(
        <img  className='poster' src={movie.image} alt='poster' />

          )
        })}
         
         </div>
    </div>
  )
}

export default RowPoster