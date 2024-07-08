import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";
import api from "../api/axios";
import styles from './SwipeDeck.module.css'; // Import the CSS module

const SwipeDeck = () => {
    const [people, setPeople] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

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
    const swiped = (direction, id) => {
        console.log("Removing: " + id);
    };

    const outOfFrame = (id) => {
        console.log(id + " left the screen!");
    };

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
                    onSwipe={(dir) => swiped(dir, person.id)}
                    onCardLeftScreen={() => outOfFrame(person.id)}
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
                                <p>Age: {person.age}</p>
                                <p>Gender: {person.gender}</p>
                            </div>
                            <img src="" alt="profile image" />
                        </div>

                    </div>
                </TinderCard>
            ))}
        </div>
    );
};

export default SwipeDeck;
