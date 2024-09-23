import React, { useEffect, useState } from "react";
import api from "../api/axios";
import "./currentUserProfile.css";
import Sidebar from "../discovery/SideBar";

const UserProfile = () => {
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const userId = sessionStorage.getItem('userId');
        const fetchProfile = async () => {
            try {
                // Update the URL to match the backend route with a URL parameter
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

    if (loading) {
        return <div className="loading">Loading...</div>;
    }

    if (error) {
        return <div className="error">{error}</div>;
    }

    return (
        <div>
            <Sidebar />
            <div className="user-profile-container">
                <div className="profile-header">
                        <img src={`https://www.loveefy.africa/uploads${profile.image_path}`} alt="Profile image" className="profile-image" />                    <div className="profile-basic-info">
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
