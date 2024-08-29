import React, { useState } from "react";
import { NavLink, useNavigate } from 'react-router-dom';
import { FaBars } from 'react-icons/fa'; // Import the hamburger icon
import styles from './Sidebar.module.css'; 

const Sidebar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [activeTab, setActiveTab] = useState('home');
    const navigate = useNavigate(); 

    const handleNavClick = (tabName, path) => {
        setActiveTab(tabName);
        setIsOpen(false); // Close sidebar after clicking a link
        navigate(path);
    };

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    };

    return (
        <>
            {/* Hamburger Icon */}
            <div className={styles.hamburger} onClick={toggleSidebar}>
                <FaBars />
            </div>

            {/* Sidebar */}
            <div className={`${styles["side-nav"]} ${isOpen ? styles.open : ''}`}>
                <h1>Loveefy</h1>
                <ul>
                    <li
                        className={activeTab === 'home' ? styles.active : ''}
                        onClick={() => handleNavClick('home', '/discovery/home')}
                    >
                        <div className={styles["nav-item"]}>Home</div>
                    </li>
                    <li
                        className={activeTab === 'chats' ? styles.active : ''}
                        onClick={() => handleNavClick('chats', '/discovery/chats')}
                    >
                        <div className={styles["nav-item"]}>Messages</div>
                    </li>
                    <li
                        className={activeTab === 'notifications' ? styles.active : ''}
                        onClick={() => handleNavClick('notifications', '/discovery/notifications')}
                    >
                        <div className={styles["nav-item"]}>Notifications</div>
                    </li>
                    <li
                        className={activeTab === 'settings' ? styles.active : ''}
                        onClick={() => handleNavClick('settings', '/discovery/settings')}
                    >
                        <div className={styles["nav-item"]}>Settings</div>
                    </li>
                    <li
                        className={activeTab === 'upgrade' ? styles.active : ''}
                        onClick={() => handleNavClick('upgrade', '/discovery/upgrade')}
                    >
                        <div className={styles["nav-item"]}>Upgrade</div>
                    </li>
                    <li
                        className={activeTab === 'feedback' ? styles.active : ''}
                        onClick={() => handleNavClick('feedback', '/discovery/feedback')}
                    >
                        <div className={styles["nav-item"]}>Feedback</div>
                    </li>
                </ul>
            </div>
        </>
    );
};

export default Sidebar;
