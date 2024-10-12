import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../api/axios';

const Gallery = () => {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const location = useLocation();

    // Helper function to extract query params
    const getUserIdFromQuery = () => {
        const params = new URLSearchParams(location.search);
        return params.get('userId');
    };

    useEffect(() => {
        const userId = getUserIdFromQuery();  // Extract userId from query string
        console.log("userId from query:", userId);  // Debugging query params

        if (!userId) {
            console.error("userId is undefined or empty");
            setError("Invalid user ID");
            setLoading(false);
            return;
        }

        const fetchImages = async () => {
            const userId = getUserIdFromQuery();
            
            try {
                const response = await api.get(`/api/v1/gallery?userId=${userId}`);
                console.log("Response status:", response);
        
                if (response.status === 404) {
                    setError('No images found for this user.');
                } else {
                    console.log(response.data)
                    const data = await response.json();
                    console.log("Parsed JSON data:", data);
                    setImages(data.data || []);  
                }
            } catch (err) {
                console.error("Error fetching images:", err.message);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };
        

        fetchImages();  // Call fetchImages inside useEffect
    }, [location.search]);  // Run the effect when query params (search) change

    if (loading) {
        return <p>Loading images...</p>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }

    return (
        <div className="gallery">
            {images.length === 0 ? (
                <p>No images found.</p>
            ) : (
                images.map((image) => (
                    <div key={image.id} className="gallery-item">
                        <img src={image.image_path} alt={`Image ${image.id}`} />
                    </div>
                ))
            )}
        </div>
    );
};

export default Gallery;
