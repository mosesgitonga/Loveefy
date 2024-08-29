import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import api from "../api/axios";
import "./DualSelect.css"
import PrivateMessage from "../messages/sockets";

const DualSelect = () => {
    const [people, setPeople] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentUserId, setCurrentUserId] = useState(null);

    const navigate = useNavigate(); 

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const response = await api.get('/api/v1/recommendations');
                const fetchedRecommendations = response.data;
                setPeople(fetchedRecommendations);
            } catch (error) {
                console.error('Error fetching matches', error);
                setError(error.response?.data || "An Error Occurred");
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations();
    }, []);

    useEffect(() => {
        const userId = sessionStorage.getItem("userId");
        if (userId) {
            setCurrentUserId(userId);
        } else {
            console.error("No userId found in sessionStorage");
            navigate('/login'); 
        }
    }, [navigate]);

    const handleLike = async (person) => {
        try {
            let liked_id;
    
            if (currentUserId === person.user_id1) {
                liked_id = person.user_id2;
            } else {
                liked_id = person.user_id1;
            }
    
            const response = await api.post('/api/v1/likes', {
                liker_id: currentUserId,
                liked_id: liked_id
            });
    
            if (response.data.message === "it's a match!") {
                alert(`You have matched with ${person.username}. Start a conversation.`);
            }
            scrollAwayProfiles();
        } catch (error) {
            console.error('Error handling like', error);
        }
    };

    const handlePass = () => {
        scrollAwayProfiles();
    };

    const scrollAwayProfiles = () => {
        setPeople(prevPeople => prevPeople.slice(2));
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dual-select-container">
            <h2>Like only one person or pass</h2>
            {people.length >= 2 ? (
                <div className="profile-pair">
                    <div className="profile">
                        <div className="profile-content" style={{ backgroundImage: `url(${people[0].image_path})` }}>
                            <h3>Username: {people[0].username}</h3>
                            <h3>Industry: {people[0].industry}</h3>
                            <h3>Country: {people[0].country}</h3>
                            <h3>Region: {people[0].region}</h3>
                            <h3>Age: {people[0].age}</h3>
                        </div>
                        <div className="actions">
                            <button onClick={() => handleLike(people[0])}>Like</button>
                            <button onClick={handlePass}>Pass</button>
                        </div>
                        
                    </div>
                    <div className="profile">
                        <div className="profile-content" style={{ backgroundImage: `url(${people[1].image_path})` }}>
                            <h3>Username: {people[1].username}</h3>
                            <h3>Industry: {people[1].industry}</h3>
                            <h3>Country: {people[1].country}</h3>
                            <h3>Region: {people[1].region}</h3>
                            <h3>Age: {people[1].age}</h3>
                        </div>
                        <div className="actions">
                            <button onClick={() => handleLike(people[1])}>Like</button>
                            <button onClick={handlePass}>Pass</button>
                        </div>
                    </div>
                </div>
            ) : (
                <div>No more profiles to show.</div>
            )}
        </div>
    );
};

export default DualSelect;
