import React, { useEffect, useState } from "react";
import api from "../api/axios";
import Sidebar from "../discovery/SideBar";
import "./notifications.css"; // Import the CSS file

const Notifications = () => {
    const [notifications, setNotifications] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNotifications = async () => {
            try {
                const response = await api.get('/api/v1/notifications');
                const fetchedNotifications = response.data.notifications || []; // Handle empty response
                setNotifications(fetchedNotifications);
                setLoading(false);
            } catch (error) {
                setError("Failed to fetch notifications.");
                setLoading(false);
            }
        };

        fetchNotifications();
    }, []); // The empty dependency array ensures this runs only once on mount

    const handleLikeBack = async (userId, notificationId) => {
        try {
            await api.post('/api/v1/like-back', { userId, notificationId });
            // Optionally, you can refresh the notifications or provide feedback to the user
            // For instance, you could remove the notification from the list
            setNotifications(notifications.filter(notification => notification.id !== notificationId));
        } catch (error) {
            console.error("Failed to like back:", error);
        }
    }

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="notificationContainer">
            <div>
                <Sidebar />
            </div>
            <div className="notifications-container">
                <h2>Notifications</h2>
                {notifications.length > 0 ? (
                    <ul className="notifications-list">
                        {notifications.map((notification) => (
                            <li key={notification.id} className="notification-item">
                                <span className="notification-message">
                                    {notification.message}
                                </span>
                                <span className="notification-username">
                                    - {notification.from_username}
                                </span>
                                <button
                                    onClick={() => handleLikeBack(notification.from_user_id, notification.id)}
                                    className="like-back-button"
                                >
                                    Like Back
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
