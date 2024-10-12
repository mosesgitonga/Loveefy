import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import api from '../api/axios';
import './gallerPage.css'

const Gallery = () => {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const location = useLocation();

    const getUserIdFromQuery = () => {
        const params = new URLSearchParams(location.search);
        return params.get('userId');
    };

    useEffect(() => {
        const userId = getUserIdFromQuery();
        console.log("userId from query:", userId);

        if (!userId) {
            console.error("userId is undefined or empty");
            setError("Invalid user ID");
            setLoading(false);
            return;
        }

        const fetchImages = async () => {
            try {
                const response = await api.get(`/api/v1/gallery?userId=${userId}`);
                console.log("Response status:", response);

                if (response.status === 404) {
                    setError('No images found for this user.');
                } else {
                    const data = response.data;
                    console.log("Parsed data:", data);
                    setImages(data.data || []);
                }
            } catch (err) {
                console.error("Error fetching images:", err.message);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchImages();
    }, [location.search]);

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
                        <img src={`www.loveefy.africa/uploads${image.image_path}`} alt={`Image ${image.id}`} />
                    </div>
                ))
            )}
        </div>
    );
};

export default Gallery;