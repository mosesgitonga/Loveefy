import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";
import api from "../api/axios";

const SwipeDeck = () => {
    const [people, setPeople] = useState([]); // Initialize as an empty array
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Fetching a batch of 50 potential matches
        const fetchMatches = async () => {
            try {
                const response = await api.get('/api/v1/recommendations');
                console.log(response.data)
                setPeople(response.data); // Assuming the API response structure
            } catch (error) {
                console.error('Error fetching matches:', error);
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchMatches();
    }, []);

    const swiped = (direction, nameToDelete) => {
        console.log("Removing: " + nameToDelete);
    };

    const outOfFrame = (name) => {
        console.log(name + " left the screen!");
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!people || people.length === 0) {
        return <div>No matches found.</div>;
    }

    return (
        <div className="swipe-deck">
            {people.map((person) => (
                <TinderCard
                    className="swipe"
                    key={person.name}
                    onSwipe={(dir) => swiped(dir, person.name)}
                    onCardLeftScreen={() => outOfFrame(person.name)}
                >
                    <div
                        style={{ backgroundImage: 'url(' + person.url + ')' }}
                        className="card"
                    >
                        <h3>{person.name}</h3>
                    </div>
                </TinderCard>
            ))}
        </div>
    );
};

export default SwipeDeck;
