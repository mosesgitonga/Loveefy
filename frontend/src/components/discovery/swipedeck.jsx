import React, { useState, useEffect, useCallback } from "react";
import TinderCard from "react-tinder-card";
import api from "../api/axios";
import styles from './SwipeDeck.module.css'; // Import the CSS module

const SwipeDeck = () => {
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
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };


        fetchMatches();
    }, []);

    console.log(people)
    const swiped = useCallback((direction, id) => {
        if (direction === 'right') {
            setLikedUsers(prevLikedUsers => [...prevLikedUsers, id]);
            
        } else if (direction === 'left') {
            console.log("Pass");
        }
        console.log("Removing: " + id);
    }, []);

    console.log(likedUsers)

    const outOfFrame = (id) => {
        console.log(id + " left the screen!");
    };


    const postLikes = async () => {
        try {
            if (likedUsers.length === 1) {
                const response = api.post('/api/v1/likes', { likedUsers })
                if (response !== 200) {
                    console.log('unable to create the likes')
                }
                console.log('liked users have been created')
                setLikedUsers([])
            }
        } catch (error) {
            console.error(error)
        }
    }

    useEffect(() => {
        if (likedUsers.length === 1) {
            postLikes();
        }
    }, [likedUsers])

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
                    onSwipe={(dir)=> swiped(dir, person.user_id2)}
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
                        <div className={styles.sideIcons}>

                        </div>

                    </div>
                </TinderCard>
            ))}
        </div>
    );
};

export default SwipeDeck;
