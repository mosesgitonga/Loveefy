import React, { useState } from "react";
import Sidebar from "./SideBar";
import SwipeDeck from "./swipedeck";


const Discovery = () => {
    return (
        <div className="window">
        <Sidebar />
        <div>
            <SwipeDeck />    
        </div>            
        </div>
    )
}

export default Discovery;