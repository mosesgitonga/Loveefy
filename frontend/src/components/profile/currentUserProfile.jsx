import React, { useEffect, useState } from "react";
import api from "../api/axios";
import "./currentUserProfile.css";
import Sidebar from "../discovery/SideBar";
import { useNavigate } from 'react-router-dom';
import { FaCamera } from "react-icons/fa";

const UserProfile = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const userId = sessionStorage.getItem('userId');
        const fetchProfile = async () => {
            try {
                const response = await api.get(`/api/v1/profile/${userId}`);
                console.log(response.data);
                setProfile(response.data.message); // Adjust if the response structure differs
            } catch (error) {
                setError("Failed to fetch profile details.");
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, []);

    const handleUploadClick = () => {
        navigate('/upload')
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
                        {/* Camera icon overlay */}
                        <div className="camera-icon" onClick={handleUploadClick}>
                            <FaCamera size={20} />
                        </div>
                    </div>
                    <div className="profile-basic-info">
                        <h1 className="username">{profile.username}</h1>
                        <p className="career">{profile.career} - {profile.industry_major}</p>
                        <p className="location">{profile.region}, {profile.sub_region}, {profile.country}</p>
                    </div>
                </div>

                <div className="profile-details">
                    <h2>About</h2>
                    <p><strong>Date of Birth:</strong> {new Date(profile.dob).toLocaleDateString()}</p>
                    <p><strong>Education Level:</strong> {profile.education_level}</p>
                    <p><strong>Employment:</strong> {profile.employment}</p>
                    <p><strong>Schooling:</strong> {profile.is_schooling ? "Yes" : "No"}</p>
                    <p><strong>Has Child:</strong> {profile.has_child ? "Yes" : "No"}</p>
                    <p><strong>Mobile Number:</strong> {profile.mobile_no}</p>
                    <p><strong>Joined At:</strong> {new Date(profile.joined_at).toLocaleDateString()}</p>
                </div>
            </div>
        </div>
    );
};

export default UserProfile;
