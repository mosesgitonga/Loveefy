import React, { useState, useEffect, useCallback } from "react";
import { useNavigate } from 'react-router-dom';
import { FaBars, FaBell } from 'react-icons/fa'; 
import styles from './Sidebar.module.css';
import api from "../api/axios";

const Sidebar = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [activeTab, setActiveTab] = useState('home');
    const [notificationCount, setNotificationCount] = useState(0);
    const [unreadMsgSize, setUnreadMsgSize] = useState(0);
    const navigate = useNavigate();

    const handleNavClick = (tabName, path) => {
        setActiveTab(tabName);
        navigate(path);
    };

    const fetchNotificationCount = useCallback(async () => {
        try {
            const response = await api.get('/api/v1/notification_count');
            setNotificationCount(response.data.notification_count);
        } catch (err) {
            console.error('Failed to fetch notifications:', err);
        }
    }, []);

    const fetchUnreadMessages = useCallback(async () => {
        try {
            const response = await api.get('/api/v1/all_unread/count');
            setUnreadMsgSize(response.data.size);
        } catch (error) {
            console.error('Error fetching unread messages count:', error.message);
        }
    }, []);

    const handleGetLocation = () => {
        if (!navigator.geolocation) {
            alert('Geolocation is not supported by this browser.');
            return;
        }
        
        navigator.geolocation.getCurrentPosition(
            async (position) => {
                const { latitude, longitude } = position.coords;
                try {
                    await api.post('/api/v1/geo_location', { latitude, longitude });
                } catch (error) {
                    console.error('Error sending location:', error);
                }
            },
            (error) => {
                console.error('Error getting location:', error.message);
                alert('Unable to retrieve your location.');
            }
        );
    };

    useEffect(() => {
        fetchNotificationCount();
        const notificationIntervalId = setInterval(fetchNotificationCount, 25000);

        return () => clearInterval(notificationIntervalId);
    }, [fetchNotificationCount]);

    useEffect(() => {
        fetchUnreadMessages();
        const messageIntervalId = setInterval(fetchUnreadMessages, 30000);

        return () => clearInterval(messageIntervalId);
    }, [fetchUnreadMessages]);

    const toggleSidebar = () => setIsOpen(prev => !prev);

    return (
        <>
            <button 
                className={styles.hamburger} 
                onClick={toggleSidebar} 
                aria-expanded={isOpen} 
                aria-label="Toggle Sidebar"
            >
                <FaBars />
            </button>

            <nav className={`${styles.sideNav} ${isOpen ? styles.open : ''}`}>
                <h1>Loveefy</h1>
                <ul>
                    <li
                        className={activeTab === 'home' ? styles.active : ''}
                        onClick={() => handleNavClick('home', '/discovery/home')}
                    >
                        <div className={styles.navItem}>Home</div>
                    </li>

                    <li
                        className={activeTab === 'chats' ? styles.active : ''}
                        onClick={() => handleNavClick('chats', '/discovery/chats')}
                    >
                        <div className={styles.navItem}>
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
                        <div className={styles.navItem}>
                            Notifications
                            {notificationCount > 0 && (
                                <span className={styles.unreadBadge}>
                                    <FaBell /> {notificationCount}
                                </span>
                            )}
                        </div>
                    </li>

                    <li
                        className={activeTab === 'profile' ? styles.active : ''}
                        onClick={() => handleNavClick('profiles', '/profile')}
                    >
                        <div className={styles.navItem}>Profile</div>
                    </li>

                    <li
                        className={activeTab === 'settings' ? styles.active : ''}
                        onClick={() => handleNavClick('settings', '/discovery/settings')}
                    >
                        <div className={styles.navItem}>Settings</div>
                    </li>

                    <li
                        className={activeTab === 'upgrade' ? styles.active : ''}
                        onClick={() => handleNavClick('upgrade', '/hello_user')}
                    >
                        <div className={styles.navItem}>Upgrade</div>
                    </li>

                    <li
                        className={activeTab === 'feedback' ? styles.active : ''}
                        onClick={() => handleNavClick('feedback', '/feedback')}
                    >
                        <div className={styles.navItem}>Feedback</div>
                    </li>
                </ul>
            </nav>
        </>
    );
};

export default Sidebar;
