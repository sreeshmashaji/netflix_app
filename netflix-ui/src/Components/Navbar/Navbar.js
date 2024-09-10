import React from 'react'
import './Navbar.css'

function Navbar() {
  return (
    <div className='navbar'>
        <img className="logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Netflix_2015_logo.svg/1920px-Netflix_2015_logo.svg.png" alt="Netflix image" />
        <div className='nav-links'>
        <a href='/home'>Home</a>
        <a href='/tvshows'>TV Shows</a>
        <a href='/movies'>Movies</a>
        <a href='/new-popular'>New & Popular</a>
        <a href='/mylist'>My List</a>
      </div>
        <img className='avatar' src="https://i.pinimg.com/originals/0d/dc/ca/0ddccae723d85a703b798a5e682c23c1.png" alt="avatar" />
        
    </div>
  )
}

export default Navbar