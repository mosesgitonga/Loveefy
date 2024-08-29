import React, { useState } from "react";
import Sidebar from "./SideBar";
import styles from "./discovery.module.css";
import DualSelect from "./DualSelect";

const Discovery = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className={styles.window}>
            <Sidebar isOpen={isOpen} toggleSidebar={toggleSidebar} />
            <div className={styles.swipedeck}>
                <DualSelect />
            </div>
        </div>
    );
};

export default Discovery;
