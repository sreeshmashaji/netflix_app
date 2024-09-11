import React ,{useEffect,useState} from 'react'
import './RowPoster.css'
import axios from 'axios'


function RowPoster(props) {

  const [movies, setMovies] = useState([])
  useEffect(() => {

    axios.get(props.url)
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
        
        <h2>{props.title}</h2>
        <div className='posters'>
        {movies.map((movie)=>{
          return(
        <img  className={ props.isSmall ?  'smallPoster': 'poster' }src={movie.image} alt='poster' />

          )
        })}
         
         </div>
    </div>
  )
}

export default RowPoster