import React, { useEffect, useState } from "react";
import api from "../api/axios";
import Sidebar from "../discovery/SideBar";
import "./notifications.css";

const Notifications = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [dropdownVisible, setDropdownVisible] = useState({}); // State to manage dropdown visibility

    useEffect(() => {
        const fetchNotifications = async () => {
            try {
                const { data } = await api.get('/api/v1/notifications');
                setNotifications(data.notifications || []);
            } catch (error) {
                setError("Failed to fetch notifications.");
            } finally {
                setLoading(false);
            }
        };

        fetchNotifications();
    }, []);

    const handleLikeBack = async (userId, notificationId) => {
        try {
            await api.post('/api/v1/like-back', { userId, notificationId });
            
            const notificationElement = document.getElementById(`notification-${notificationId}`);
            if (notificationElement) {
                notificationElement.classList.add('fade-out');
                
                setTimeout(() => {
                    setNotifications((prevNotifications) =>
                        prevNotifications.filter(notification => notification.id !== notificationId)
                    );
                }, 500); 
            }
        } catch (error) {
            console.error("Failed to like back:", error);
        }
    };

    const handleReject = async (notificationId) => {
        try {   
            response =  await api.delete('/api/v1/reject', {rejected_id})
            // Remove the rejected notification from UI
            setNotifications((prevNotifications) =>
                prevNotifications.filter(notification => notification.id !== notificationId)
            );
        } catch (error) {
            console.error("Failed to reject notification:", error);
        }
    };

    const toggleDropdown = (notificationId) => {
        setDropdownVisible(prevState => ({
            ...prevState,
            [notificationId]: !prevState[notificationId]
        }));
    };

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (error) {
        return (
            <div className="error">
                {error}
                <button onClick={() => fetchNotifications()}>Retry</button>
            </div>
        );
    }

    return (
        <div className="notificationContainer">
            <Sidebar />
            <div className="notifications-container">
                <h2>Notifications</h2>
                {notifications.length > 0 ? (
                    <ul className="notifications-list">
                        {notifications.map((notification) => (
                            <li
                                key={notification.id}
                                id={`notification-${notification.id}`}
                                className="notification-item"
                            >
                                <span className="notification-message">{notification.message}</span>
                                <span className="notification-username">- {notification.from_username}</span>
                                <div className="profile-info">
                                    <div className="profile" onClick={() => toggleDropdown(notification.id)}>
                                        View Profile
                                        {dropdownVisible[notification.id] && (
                                            <div className="dropdown">
                                                <div>
                                                    <img src={`https://www.loveefy.africa/uploads${notification.image_path}`} alt="profile image" />
                                                    <p>Industry: {notification.industry}</p>
                                                    <p>Career: {notification.career}</p>
                                                    <p>Age: {notification.age}</p>
                                                    <p>Gender: {notification.gender}</p>
                                                    <p>Education Level: {notification.education_level}</p>
                                                </div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                                <button
                                    onClick={() => handleLikeBack(notification.from_user_id, notification.id)}
                                    className="like-back-button"
                                >
                                    Like Back
                                </button>
                                <button
                                    onClick={() => handleReject(notification.id)}
                                    className="reject"
                                >
                                    Reject
                                </button>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <div className="no-notifications">Notifications will appear here.</div>
                )}
            </div>
        </div>
    );
};

export default Notifications;
