import Banner from "./Components/Banner/Banner";
import Navbar from "./Components/Navbar/Navbar";

import React from "react";
import RowPoster from "./Components/RowPoster/RowPoster";
import {comedyUrl,horrorUrl,originalUrl,romanceUrl} from './Constants/Constant'


function App() {
  return (
    <div>
     <Navbar/>
     <Banner/>
     <RowPoster url={originalUrl} title="Netflix Originals"/>
     <RowPoster url={horrorUrl} title="Horror" isSmall/>
     <RowPoster url={comedyUrl} title="Comedy" isSmall/>

     <RowPoster  url={romanceUrl} title="Romance" isSmall/>


    </div>
  );
}

export default App;
