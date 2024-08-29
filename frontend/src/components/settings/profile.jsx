import React, { useState, useEffect } from 'react';
import axios from 'axios';
import api from '../api/axios';
import './ProfileSettings.css';

const ProfileSettings = ({ userId }) => {
    const [username, setUsername] = useState('');
    const [industry, setIndustry] = useState('');
    const [country, setCountry] = useState('');
    const [region, setRegion] = useState('');
    const [subRegion, setSubRegion] = useState('');
    const [career, setCareer] = useState('');
    const [dob, setDob] = useState('');

    useEffect(() => {
        // Fetch the existing user profile
        const fetchProfile = async () => {
            try {
                const response = await api.get(`/api/v1/profile`);
                const profileData = response.data;
                console.log(profileData)
                setUsername(profileData.username);
                setIndustry(profileData.industry);
                setCareer(profileData.career);
                setDob(profileData.dob);
            } catch (error) {
                console.error('Error fetching profile data:', error.response?.data?.error || error.message);
            }
        };

        fetchProfile();
    }, [userId]);

    const handleSave = async () => {
        try {
            const profileData = {
                username,
                industry,
                career,
                dob
            };

            const response = api.patch('/api/v1/profiles/update', profileData);
            alert(response.data.message); // Display success message
        } catch (error) {
            alert('Error updating profile: ' + error.response?.data?.error || error.message);
        }
    };

    return (
        <div className="profile-settings">
            <h2>Update Profile</h2>
            <div className="form-group">
                <label htmlFor="username">Username</label>
                <input
                    type="text"
                    id="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
            </div>
            <div className="form-group">
                <label htmlFor="industry_major">
                    Industry Major:
                    <select
                        id="industry_major"
                        name="industry_major"
                        value={industry}
                        onChange={(e) => setIndustry(e.target.value)}
                        className="industry_major"
                    >
                        <option value="" label="Select industry major" />
                        <option value="health" label="Health" />
                        <option value="it" label="IT" />
                        <option value="finance" label="Finance" />
                        <option value="business" label="Business" />
                        <option value="law" label="Law" />
                        <option value="engineering" label="Engineering" />
                        <option value="education" label="Education" />
                        <option value="scientific_research" label="Scientific Research" />
                        <option value="manufacturing" label="Manufacturing" />
                        <option value="retail" label="Retail" />
                        <option value="transportation" label="Transportation" />
                        <option value="agriculture" label="Agriculture" />
                        <option value="hospitality" label="Hospitality" />
                        <option value="construction" label="Construction" />
                        <option value="real_estate" label="Real Estate" />
                        <option value="security" label="Security" />
                        <option value="others" label="Others" />
                    </select>
                </label>
            </div>
            <div className="form-group">
                <label htmlFor="career">Career</label>
                <input
                    type="text"
                    id="career"
                    value={career}
                    onChange={(e) => setCareer(e.target.value)}
                />
            </div>
            <div className='form-group'>
                <label htmlFor="dob">Date of Birth</label>
                <input
                    type="date"
                    id="dob"
                    value={dob}
                    onChange={(e) => setDob(e.target.value)}
                    required
                />
            </div>
            <button className="save-btn" onClick={handleSave}>Save</button>
        </div>
    );
};

export default ProfileSettings;
