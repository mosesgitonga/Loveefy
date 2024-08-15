import React, { useState } from "react";
import Sidebar from "./SideBar";
import SwipeDeck from "./swipedeck";
import styles from "./discovery.module.css"
import DualSelect from "./DualSelect";


const Discovery = () => {
    return (
        <div className={styles.window}>
            <Sidebar />
            <div className={styles.swipedeck}>
                <DualSelect />
            </div>
        </div>
    )
}

export default Discovery;