import React, { useState } from 'react';
import './ProfileSettings.css'; // Import the CSS file for styling

const ProfileSettings = () => {
    const [username, setUsername] = useState('');
    const [industry, setIndustry] = useState('');
    const [profilePicture, setProfilePicture] = useState(null);

    const handleProfilePictureChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            setProfilePicture(URL.createObjectURL(file));
        }
    };

    const handleSave = () => {
        // Handle saving the profile settings (e.g., send to server)
        alert('Profile settings saved!');
    };

    return (
        <div className="profile-settings">
            <h2>Profile Settings</h2>
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
                <label htmlFor="industry">Industry</label>
                <textarea
                    id="industry"
                    value={industry}
                    onChange={(e) => setIndustry(e.target.value)}
                ></textarea>
            </div>
            <button className="save-btn" onClick={handleSave}>Save</button>
        </div>
    );
};

export default ProfileSettings;
