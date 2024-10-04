import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import './superAdmin.css';
import UserMap from './mapComponent';

const SuperAdminPage = () => {
    const [userCount, setUserCount] = useState(0);
    const [users, setUsers] = useState([]);
    const [feedbacks, setFeedbacks] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [mapVisible, setMapVisible] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);
    const [activeSection, setActiveSection] = useState('dashboard'); // New state for navigation

    // Fetch user count
    const fetchUserCount = async () => {
        setLoading(true);
        try {
            const response = await api.get('/api/v1/auth/users/count');
            setUserCount(response.data);
        } catch (err) {
            console.error('Error fetching user count:', err);
            setError('Failed to fetch user count. Please try again later.');
        } finally {
            setLoading(false);
        }
    };

    // Fetch all users
    const fetchUsers = async () => {
        try {
            const response = await api.get('/api/v1/auth/users');
            setUsers(response.data);
        } catch (err) {
            console.error('Error fetching users:', err);
            setError('Failed to fetch user list.');
        }
    };

    // Fetch feedbacks
    const fetchFeedbacks = async () => {
        try {
            const response = await api.get('/api/v1/feedback');
            setFeedbacks(response.data);
        } catch (err) {
            console.error('Error fetching feedbacks:', err);
            setError('Failed to fetch feedbacks.');
        }
    };

    useEffect(() => {
        fetchUserCount();
        fetchUsers();
        fetchFeedbacks();
        const intervalId = setInterval(fetchUserCount, 600000);
        return () => clearInterval(intervalId);
    }, []);

    // Toggle map visibility
    const toggleMapVisibility = () => {
        setMapVisible((prevVisible) => !prevVisible);
    };

    // View user details
    const viewUserProfile = (user) => {
        setSelectedUser(user); // Set the selected user for details view
    };

    // Navigation handler
    const handleSectionChange = (section) => {
        setActiveSection(section);
        setSelectedUser(null); // Reset selected user when switching sections
    };

    return (
        <div className="admin-container">
            {/* Sidebar for navigation */}
            <nav className="sidebar">
                <h1 className="sidebar-title">God's Eye</h1>
                <ul>
                    <li className={activeSection === 'dashboard' ? 'active' : ''} onClick={() => handleSectionChange('dashboard')}>
                        Dashboard
                    </li>
                    <li className={activeSection === 'users' ? 'active' : ''} onClick={() => handleSectionChange('users')}>
                        Registered Users
                    </li>
                    <li className={activeSection === 'feedback' ? 'active' : ''} onClick={() => handleSectionChange('feedback')}>
                        User Feedback
                    </li>
                    <li className={activeSection === 'map' ? 'active' : ''} onClick={() => handleSectionChange('map')}>
                        User Map
                    </li>
                </ul>
            </nav>

            <div className="admin-dashboard">
                {/* Dashboard section */}
                {activeSection === 'dashboard' && (
                    <>
                        <h2 id='dashboard-head'>Admin Dashboard</h2>
                        {loading ? (
                            <p>Loading...</p>
                        )  : (
                            <div className="stat-section">
                                <div className='registered'>
                                    <p className="stat-text">{userCount}</p>
                                    <p>registered</p>
                                </div>
                            </div>
                        )}
                    </>
                )}

                {/* User list section */}
                {activeSection === 'users' && (
                    <div className="user-list-section">
                        <h2>Registered Users</h2>
                        <table className="user-table">
                            <thead>
                                <tr>
                                    <th>Username</th>
                                    <th>Email</th>
                                    <th>Registration Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {users.map((user) => (
                                    <tr key={user.id}>
                                        <td>{user.username}</td>
                                        <td>{user.email}</td>
                                        <td>{new Date(user.createdAt).toLocaleDateString()}</td>
                                        <td>
                                            <button className="view-profile-button" onClick={() => viewUserProfile(user)}>
                                                View Profile
                                            </button>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>

                        {/* User profile details */}
                        {selectedUser && (
                            <div className="user-details-section">
                                <h2>{selectedUser.username}'s Profile</h2>
                                <p>Email: {selectedUser.email}</p>
                                <p>Joined on: {new Date(selectedUser.createdAt).toLocaleDateString()}</p>
                                <p>Last Login: {selectedUser.lastLogin ? new Date(selectedUser.lastLogin).toLocaleDateString() : 'N/A'}</p>
                                <p>Recent Activities: {selectedUser.activities ? selectedUser.activities.join(', ') : 'No activities'}</p>
                                <button onClick={() => setSelectedUser(null)}>Close</button>
                            </div>
                        )}
                    </div>
                )}

                {/* Feedback section */}
                {activeSection === 'feedback' && (
                    <div className="feedback-section">
                        <h2>User Feedback</h2>
                        <table className="feedback-table">
                            <thead>
                                <tr>
                                    <th>User</th>
                                    <th>Feedback</th>
                                    <th>Date</th>
                                </tr>
                            </thead>
                            <tbody>
                                {feedbacks.map((feedback) => (
                                    <tr key={feedback.id}>
                                        <td>{feedback.username}</td>
                                        <td>{feedback.content}</td>
                                        <td>{new Date(feedback.date).toLocaleDateString()}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}

                {/* Map section */}
                {activeSection === 'map' && (
                    <div className="map-section">
                        <button className="map-toggle-button" onClick={toggleMapVisibility}>
                            {mapVisible ? 'Hide Map' : 'Show Map'}
                        </button>
                        {mapVisible && <UserMap />}
                    </div>
                )}
            </div>
        </div>
    );
};

export default SuperAdminPage;
