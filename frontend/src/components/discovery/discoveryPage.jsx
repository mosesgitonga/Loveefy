import React, { useState } from "react";
import Sidebar from "./SideBar";
import SwipeDeck from "./swipedeck";
import styles from "./discovery.module.css"


const Discovery = () => {
    return (
        <div className={styles.window}>
            <Sidebar />
            <div className={styles.swipedeck}>
                <SwipeDeck />           
            </div>
        </div>
    )
}

export default Discovery;