import React, { useState } from "react";
import { NavLink, useNavigate } from 'react-router-dom';
import styles from './Sidebar.module.css'; 

const Sidebar = () => {
    const [activeTab, setActiveTab] = useState('home');
    const navigate = useNavigate(); 

    const handleNavClick = (tabName, path) => {
        setActiveTab(tabName);
        navigate(path);
    };

    return (
        <div className={styles["side-nav"]}>
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
    );
};

export default Sidebar;
