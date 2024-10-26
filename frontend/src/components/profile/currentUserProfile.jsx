import React, { useEffect, useState } from "react";
import api from "../api/axios";
import "./currentUserProfile.css";
import Sidebar from "../discovery/SideBar";
import { useNavigate, useParams } from 'react-router-dom';
import { FaCamera, FaArrowRight } from "react-icons/fa";
import ChatBox from "../messages/chatBox";

const UserProfile = () => {
    const { userId } = useParams();
    const { roomId } = useState('')
    const currentUserId = sessionStorage.getItem('userId');
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await api.get(`/api/v1/profile/${userId}`);
                setProfile(response.data.message); 
            } catch (error) {
                setError("Failed to fetch profile details.");
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, [userId]);

    const handleGalleryClick = (userId) => {
        navigate(`/gallery?userId=${userId}`);
    };

    const handleUploadClick = () => {
        navigate('/upload');
    };

    const handleSendMessage = () => {
         navigate(`/c/${roomId}`);
    };

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div className="profile-page-container">
            <Sidebar />
            <div className="user-profile-content">
                <div className="profile-header">
                    <div className="profile-image-wrapper">
                        <img
                            src={`https://www.loveefy.africa/uploads${profile.image_path}`}
                            alt="Profile"
                            className="profile-image"
                        />
                        {currentUserId === profile.user_id && (
                            <div className="camera-icon" onClick={handleUploadClick}>
                                <FaCamera size={20} />
                            </div>
                        )}
                    </div>
                    <div className="profile-basic-info">
                        <h1 className="username">{profile.username}</h1>
                        <p className="career">{profile.career} - {profile.industry_major}</p>
                        <p className="location">{profile.sub_region}, {profile.region} - {profile.country}</p>
                        <p className="bio">{profile.bio}</p>
                    </div>
                </div>

                <div className="profile-details">
                    <div className="details-card">
                        <h2>About</h2>
                        <div className="about-features">
                            <button className="gallery-button" onClick={() => handleGalleryClick(userId)}>
                                View Gallery <FaArrowRight />
                            </button>
                        </div>
                        <p><strong>Age:</strong>{profile.age}</p>
                        <p><strong>Education Level:</strong> {profile.education_level}</p>
                        <p><strong>Employment:</strong> {profile.employment}</p>
                        <p><strong>Is Schooling:</strong> {profile.is_schooling}</p>
                        <p><strong>Has Child:</strong> {profile.has_child }</p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
