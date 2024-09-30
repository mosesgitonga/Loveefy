import React, { useEffect, useState } from 'react';
import api from '../api/axios'

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
        <div>
            <h1>Super Admin Dashboard</h1>
            <p id="userCount">Number of registered users: {userCount}</p>
        </div>
    );
};

export default SuperAdminPage;
