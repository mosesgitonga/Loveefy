import React, { useEffect, useState } from 'react';
import api from '../api/axios';
import './superAdmin.css';
import UserMap from './mapComponent';

const SuperAdminPage = () => {
    const [userCount, setUserCount] = useState(0);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [mapVisible, setMapVisible] = useState(false); // State to control map visibility

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

    useEffect(() => {
        fetchUserCount();
        const intervalId = setInterval(fetchUserCount, 600000);
        return () => clearInterval(intervalId);
    }, []);

    const toggleMapVisibility = () => {
        setMapVisible(prevVisible => !prevVisible); // Toggle map visibility
    };

    return (
        <div className='superContainer'>
            <div className='superAdminDashboard'>
                <h1>Loveefy God's Eye</h1>
                {loading ? (
                    <p>Loading...</p>
                ) : error ? (
                    <p className="error">{error}</p>
                ) : (
                    <p id="userCount">Registered Users: {userCount}</p>
                )}
                <button className="toggleMapButton" onClick={toggleMapVisibility}>
                    {mapVisible ? 'Hide Map' : 'Show Map'} 
                </button>
                {mapVisible && <UserMap />} 
            </div>
        </div>
    );
};

export default SuperAdminPage;
