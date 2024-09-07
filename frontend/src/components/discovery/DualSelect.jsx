import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import api from "../api/axios";
import "./DualSelect.css"

const DualSelect = () => {
    const [people, setPeople] = useState([]);
    const [profilesToShow, setProfilesToShow] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentUserId, setCurrentUserId] = useState(null);
    const [currentIndex, setCurrentIndex] = useState(0);
    
    const navigate = useNavigate(); 

    useEffect(() => {
        const fetchRecommendations = async () => {
            try {
                const storedProfiles = sessionStorage.getItem('profiles');
                const storedIndex = sessionStorage.getItem('currentIndex');
                
                if (storedProfiles) {
                    const profiles = JSON.parse(storedProfiles);
                    const index = parseInt(storedIndex, 10) || 0;
                    setPeople(Array.isArray(profiles) ? profiles : []);
                    setCurrentIndex(index);
                    setProfilesToShow(Array.isArray(profiles) ? profiles.slice(index, index + 2) : []);
                } else {
                    const response = await api.get('/api/v1/recommendations');
                    if (response.status === 200) {  // Check for successful response
                        const fetchedRecommendations = response.data;
                        setPeople(Array.isArray(fetchedRecommendations) ? fetchedRecommendations : []);
                        sessionStorage.setItem('profiles', JSON.stringify(fetchedRecommendations));
                        setProfilesToShow(fetchedRecommendations.slice(0, 2));
                    } else {
                        throw new Error('Failed to fetch recommendations');
                    }
                }
                setLoading(false);
            } catch (error) {
                console.error('Error fetching matches:', error);
                setError(error.message || "An Error Occurred");
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
            updateProfiles();
        } catch (error) {
            console.error('Error handling like', error);
            alert('There was an error processing your like. Please try again.');
        }
    };

    const handlePass = () => {
        updateProfiles();
    };

    const updateProfiles = () => {
        setCurrentIndex(prevIndex => {
            const nextIndex = prevIndex + 2;
            if (nextIndex < people.length) {
                sessionStorage.setItem('currentIndex', nextIndex); 
                setProfilesToShow(people.slice(nextIndex, nextIndex + 2));
            } else {
                setProfilesToShow([]); 
            }
            return nextIndex;
        });
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dual-select-container">
            <h2>Like only one person or pass</h2>
            {Array.isArray(profilesToShow) && profilesToShow.length >= 2 ? (
                <div className="profile-pair">
                    {profilesToShow.map((profile, index) => (
                        <div className="profile" key={index}>
                            <div className="profile-content" style={{ backgroundImage: `url(${profile.image_path})` }}>
                                <h3>Username: {profile.username}</h3>
                                <h3>Industry: {profile.industry}</h3>
                                <h3>Country: {profile.country}</h3>
                                <h3>Region: {profile.region}</h3>
                                <h3>Age: {profile.age}</h3>
                            </div>
                            <div className="actions">
                                <button onClick={() => handleLike(profile)}>Like</button>
                                <button onClick={handlePass}>Pass</button>
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div>No more profiles to show.</div>
            )}
        </div>
    );
};

export default DualSelect;
