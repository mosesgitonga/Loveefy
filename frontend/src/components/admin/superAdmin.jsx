import React, { useEffect, useState } from 'react';
import api from '../api/axios'
import './superAdmin.css'
import UserMap from './mapComponent';

const SuperAdminPage = () => {
    const [userCount, setUserCount] = useState(0);

    const fetchUserCount = async () => {
        try {
            const response = await api.get('/api/v1/auth/users/count');  
            const data = await response
            setUserCount(data.data);
        } catch (error) {
            console.error('Error fetching user count:', error);
        }
    };

    useEffect(() => {
        fetchUserCount();

        const intervalId = setInterval(fetchUserCount, 600000);

        // Cleanup interval when component unmounts
        return () => clearInterval(intervalId);
    }, []);

    return (
        <div className='superAdminDashboard'>
            <h1>Loveefy Super Admin Dashboard</h1>
            <p id="userCount">Registered Users: {userCount}</p>

            <UserMap />
        </div>
    );
};

export default SuperAdminPage;
