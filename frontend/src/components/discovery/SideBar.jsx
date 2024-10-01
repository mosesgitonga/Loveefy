import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { FaBars } from 'react-icons/fa'; 
import styles from './Sidebar.module.css';
import api from "../api/axios";

const Sidebar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [activeTab, setActiveTab] = useState('home');
    const [unreadMsgSize, setUnreadMsgSize] = useState(0);
    const navigate = useNavigate();

    const handleNavClick = (tabName, path) => {
        setActiveTab(tabName);
        setIsOpen(true); 
        navigate(path);
    };
    const handleGetLocation = () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const { latitude, longitude } = position.coords;
                    setLocation({ latitude, longitude });
                    
                    // Send location to backend
                    api.post('/api/v1/geo_location', { latitude, longitude })
                        .then(response => console.log('Location sent:', response))
                        .catch(error => console.error('Error sending location:', error));
                },
                (error) => {
                    console.error('Error getting location:', error.message);
                    alert('Unable to retrieve your location.');
                }
            );
        } else {
            alert('Geolocation is not supported by this browser.');
        }
    };

    useEffect(() => {
        const fetchUnreadMessages = async () => {
            try {
                const response = await api.get('/api/v1/all_unread/count');
                
                console.log(response.data.size)
                setUnreadMsgSize(response.data.size);
                
            } catch (error) {
                if (error.response) {
                    console.error('Failed to fetch unread messages count:', error.response.data);
                } else {
                    console.error('Error fetching unread messages count:', error.message);
                }
            }
        };

        // Fetch unread messages count immediately and set interval to fetch every 40 seconds
        fetchUnreadMessages();
        const intervalId = setInterval(fetchUnreadMessages, 30000);

        // Cleanup interval on component unmount
        return () => clearInterval(intervalId);
    }, []);

    const toggleSidebar = () => {
        setIsOpen(!isOpen);
    };

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
                            Messages
                            {unreadMsgSize > 0 && (
                                <span className={styles.unreadBadge}>{unreadMsgSize}</span>
                            )}
                        </div>
                    </li>
                    <li
                        className={activeTab === 'notifications' ? styles.active : ''}
                        onClick={() => handleNavClick('notifications', '/discovery/notifications')}
                    >
                        <div className={styles["nav-item"]}>Notifications</div>
                    </li>
                    <li
                        className={activeTab === 'profile' ? styles.active : ''}
                        onClick={() => handleNavClick('profiles', '/profile')}
                    >
                        <div className={styles["nav-item"]}>Profile</div>
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
                        onClick={() => handleNavClick('feedback', '/feedback')}
                    >
                        <div className={styles["nav-item"]}>Feedback</div>
                    </li>
                </ul>
            </div>
        </>
    );
};

export default Sidebar;
