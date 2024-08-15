import React, { useState, useEffect, useCallback } from "react";
import TinderCard from "react-tinder-card";
import api from "../api/axios";
import styles from './SwipeDeck.module.css';

const SwipeDeck = ({ currentUserId }) => {
    const [people, setPeople] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [likedUsers, setLikedUsers] = useState([]);

    useEffect(() => {
        const controller = new AbortController();
        const signal = controller.signal;

        const fetchMatches = async () => {
            try {
                const response = await api.get('/api/v1/recommendations', { signal });
                const fetchedPeople = response.data;
                setPeople(fetchedPeople);
            } catch (error) {
                console.error('Error fetching matches:', error);
                setError(error.response?.data || 'An error occurred');
            } finally {
                setLoading(false);
            }
        };

        fetchMatches();
    }, []);

    const swiped = useCallback((direction, person) => {
        // Determine the ID to use based on current user
        const id = person.user_id1 ? person.user_id2 : person.user_id1;
        const currentUserId = id
        console.log(`Current User ID: ${currentUserId}`);
        console.log(`Person ID: ${id}`);
        console.log(`Swipe Direction: ${direction}`);

        if (direction === 'right') {
            setLikedUsers([id])
        } else if (direction === 'left') {
            console.log("Pass");
        }
    }, [currentUserId]);

    const outOfFrame = (id) => {
        console.log(`${id} left the screen!`);
        // Call the API to send the liked users to the backend
        postLikes();
    };

    const postLikes = async () => {
        try {
            if (likedUsers.length) {
                const response = await api.post('/api/v1/likes', { likedUsers });
                if (response.status === 201) {
                    console.log('Likes have been created successfully');
                    setLikedUsers([]); // Clear the liked users after successful API call
                } else {
                    console.log('Unable to create likes');
                }
            }
        } catch (error) {
            console.error('Error posting likes:', error);
        }
    };

    useEffect(() => {
        if (likedUsers.length) {
            postLikes();
        }
    }, [likedUsers]);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!people.length) {
        return <div>No matches found.</div>;
    }

    return (
        <div className={styles['swipe-deck']}>
            {people.map((person) => (
                <TinderCard
                    className={styles.swipe}
                    key={person.id}
                    onSwipe={(dir) => swiped(dir, person)}
                    onCardLeftScreen={() => outOfFrame(person.user_id2)}
                >
                    <div className={styles.rightSide}>
                        <div className={styles.card} style={{ 
                            backgroundImage: `url(${person.image_path})`,
                            borderRadius: '50px',
                            boxShadow: '0px 10px 30px #fff',
                            display: 'flex',
                            flexDirection: 'column',
                            justifyContent: 'flex-end',
                            padding: '20px',
                            textAlign: 'left',
                            backgroundSize: 'cover',
                            backgroundPosition: 'center' 
                        }}>
                            <div className={styles.cardDetails}>
                                <h3>Username: {person.username}</h3>
                                <p>Industry: {person.industry}</p>
                                <p>Match Score: {person.score}</p>
                                <p>Country: {person.country}</p>
                                <p>Region: {person.region}</p>
                                <p>Age: {person.age}</p>
                                <p>Gender: {person.gender}</p>
                            </div>
                            <div className={styles.lowerDiv}>
                                <div>
                                    <span className={styles.likeIcon}>❤️</span> 
                                </div>
                                <img className={styles.profilePic} src={person.image_path} alt="profile image" />
                            </div>
                        </div>
                        <div className={styles.sideIcons}></div>
                    </div>
                </TinderCard>
            ))}
        </div>
    );
};

export default SwipeDeck;
