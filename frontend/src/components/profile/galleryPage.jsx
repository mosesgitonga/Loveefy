// Gallery.jsx
import React, { useEffect, useState } from 'react';

const Gallery = ({ userId }) => {
    const [images, setImages] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchImages = async () => {
            try {
                const response = await fetch(`/api/v1/gallery?userId=${userId}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch images');
                }
                const data = await response.json();
                setImages(data.data || []); // Adjust based on your JSON structure
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchImages();
    }, [userId]); // Fetch images when userId changes

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
