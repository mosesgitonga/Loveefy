import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaBars } from 'react-icons/fa'; 
import styles from './Sidebar.module.css';
import io from "socket.io-client";

let socket;

const Sidebar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [activeTab, setActiveTab] = useState('home');
    const [msgAlertCount, setMsgAlertCount] = useState(0);
    const navigate = useNavigate();

    const handleNavClick = (tabName, path) => {
        setActiveTab(tabName);
        setIsOpen(false); // Close sidebar after clicking a link
        navigate(path);
    };

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    };

    useEffect(() => {
        const token = sessionStorage.getItem('access_token');
        
            socket = io.connect('http://localhost:5000', {
                extraHeaders: {
                    Authorization: `Bearer ${token}`
            }
        
        })

        socket.on('connect', () => {
            console.log('Connected to socket.io via sidebar');
        });

        socket.on('disconnect', () => {
            console.log('Disconnected from Socket.io server');
        });

        socket.on('receive_notification', () => {
            setMsgAlertCount(prevCount => prevCount + 1);
        });

        return () => {
            if (socket) {
                socket.disconnect();
            }
        };
    }, []);

    return (
        <>
            {/* Hamburger Icon */}
            <div className={styles.hamburger} onClick={toggleSidebar} aria-expanded={isOpen} aria-label="Toggle Sidebar">
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
                        <div className={styles["nav-item"]}>
                            Messages <span>{msgAlertCount}</span>
                        </div>
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
                        onClick={() => handleNavClick('upgrade', '/hello_user')}
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
