import React from "react";
import styles from './Sidebar.module.css'; // Import the CSS module
import { useNavigate } from 'react-router-dom';

const Sidebar = () => {
    const navigate = useNavigate();

    const handleMsgClick = () => {
        navigate('/discovery/chats'); // Ensure this route exists in your routing configuration
    };

    return (
        <div className={styles["side-nav"]}>
            <h1>Loveefy</h1>
            <ul>
                <li>Home</li>
                <li onClick={handleMsgClick}>Messages</li>
                <li>Notification</li>
                <li>Payment</li>
                <li>Settings</li>
                <li>Feedback</li>
            </ul>
        </div>
    );
}

export default Sidebar;