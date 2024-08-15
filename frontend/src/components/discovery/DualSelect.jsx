import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import api from "../api/axios";
import "./DualSelect.css"
import PrivateMessage from "../messages/sockets";

const DualSelect = () => {
    const [people, setPeople] = useState([]);
    const [likedUsers, setLikedUsers] = useState([]);
    const [currentUserId, setCurrentUserId] = useState(null);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    const navigate = useNavigate(); // Initialize useNavigate at the top level

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
            navigate('/login'); // Use the navigate function to redirect to login
        }
    }, [navigate]);

    const handleLike = async (person) => {
        try {
            console.log(currentUserId);
            
            // Declare liked_id outside the if-else block
            let liked_id;
    
            if (currentUserId === person.user_id1) {
                liked_id = person.user_id2;
            } else {
                liked_id = person.user_id1;
            }
    
            console.log(person);
            
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
            {people.length >= 2 ? (
                <div className="profile-pair">
                    <div className="profile">
                        <img src={people[0].image_path} alt={people[0].username} />
                        <h3>{people[0].username}</h3>
                        <h3>{people[0].industry}</h3>
                        <button onClick={() => handleLike(people[0])}>Like</button>
                        <button onClick={handlePass}>Pass</button>
                        <PrivateMessage />
                    </div>
                    <div className="profile">
                        <img src={people[1].image_path} alt={people[1].username} />
                        <h3>{people[1].username}</h3>
                        <h3>{people[1].industry}</h3>
                        <button onClick={() => handleLike(people[1])}>Like</button>
                        <button onClick={handlePass}>Pass</button>
                        <PrivateMessage />
                    </div>
                </div>
            ) : (
                <div>No more profiles to show.</div>
            )}
        </div>
    );
};

export default DualSelect;
