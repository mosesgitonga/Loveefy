import React from "react";
import styles from './Sidebar.module.css'; // Import the CSS module

const Sidebar = () => {
    return (
        <div className={styles["side-nav"]}>
            <h1>Loveefy</h1>
            <ul>
                <li>Home</li>
                <li>Messages</li>
                <li>Notification</li>
                <li>Payment</li>
                <li>Settings</li>
                <li>Feedback</li>
            </ul>
        </div>
    );
}

export default Sidebar;