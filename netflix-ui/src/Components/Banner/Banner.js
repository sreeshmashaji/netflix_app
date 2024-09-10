import React, { useEffect } from 'react'
import './Banner.css'
import '../../App.css'
import { API_KEY  } from '../../Constants/Constant'
import axios_instance from '../../axios_instance'
// import axios from './axios';

function Banner() {
    useEffect(()=>{
        axios_instance.get(`trending/all/week?api_key=${API_KEY}&language=en-US1`).then((res)=>{
            console.log(res.data)
        })

    },[])
    return (
        <div className='banner'>
            <div className='content'>
                <h1 className='title'>Movie Name</h1>
                <div className='banner_buttons'>
                    <button className='button'>play </button>
                    <button className='button'>My List </button>

                </div>

                <h1 className='description'>Redundant alt attribute. Screen-readers already announce `img` tags as an image. You don’t need to use the words `image`, `photo,` or `picture` (or any specified custom words) in the alt prop</h1>



            </div>
            <div className='fade'></div>

        </div>
    )
}

export default Banner