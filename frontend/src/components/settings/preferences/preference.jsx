import React, { useEffect, useState } from "react";
import api from "../../api/axios";
import './preference.css'

const PreferenceForm = () => {
    const [gender, setGender] = useState('');
    const [industry_major, setIndustry_major] = useState('');
    const [career, setCareer] = useState('');
    const [minAge, setMinAge] = useState('');
    const [maxAge, setMaxAge] = useState('');
    const [educationLevel, setEducationLevel] = useState('');
    const [educationStatus, setEducationStatus] = useState('');

    useEffect(() => {
        // Fetch the existing user profile
        const fetchProfile = async () => {
            try {
                const response = await api.get(`/v1/preference`);
                const preferenceData = response.data;
                console.log(preferenceData)
                console.log(preferenceData);
                setGender(preferenceData.message.gender);
                setIndustry_major(preferenceData.message.industry_major);
                setCareer(preferenceData.message.career);
                setMinAge(preferenceData.message.min_age);
                setMaxAge(preferenceData.message.max_age);
                setEducationLevel(preferenceData.message.education_level);
                setEducationStatus(preferenceData.message.educationStatus);
            } catch (error) {
                console.error('Error fetching profile data:', error.response?.data?.error || error.message);
            }
        };

        fetchProfile();
    }, []);

    const handleSave = async () => {
        try {
            const preferenceData = {
                gender,
                industry_major,
                career,
                minAge,
                maxAge,
                educationLevel,
                educationStatus
            };

            const response = await api.patch('/v1/preferences', preferenceData);
            alert(response.data.message); // Display success message
        } catch (error) {
            alert('Error updating profile: ' + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div className="preference-settings">
            <h2>Update Preference</h2>

            <label htmlFor="gender">
                Select Preference Gender:
                <select
                    id="gender"
                    name="gender"
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    className="gender"
                >
                    <option value="" label="Select the gender you prefer" />
                    <option value="male" label="Male" />
                    <option value="female" label="Female" />
                </select>
            </label>

            <div className="form-group">
                <label htmlFor="industry_major">
                    Industry Major of your match:
                    <select
                        id="industry_major"
                        name="industry_major"
                        value={industry_major}
                        onChange={(e) => setIndustry_major(e.target.value)}
                        className="industry_major"
                    >
                        <option value="" label="Select industry major preference" />
                        <option value="health" label="Health" />
                        <option value="information technology" label="Information Technology" />
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
                <label htmlFor="career">Career preference of your match</label>
                <input
                    type="text"
                    id="career"
                    value={career}
                    onChange={(e) => setCareer(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label htmlFor="min-age">Minimum Age</label>
                <input
                    type="number"
                    id="min-age"
                    value={minAge}
                    onChange={(e) => setMinAge(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label htmlFor="max-age">Maximum Age</label>
                <input
                    type="number"
                    id="max-age"
                    value={maxAge}
                    onChange={(e) => setMaxAge(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label htmlFor="educationLevel">Education Level</label>
                <select
                    id="educationLevel"
                    name="educationLevel"
                    value={educationLevel}
                    onChange={(e) => setEducationLevel(e.target.value)}
                    className="education_level"
                >
                    <option value="" label="Select education level" />
                    <option value="kindergarten" label="Kindergarten graduate" />
                    <option value="primary" label="Primary school graduate" />
                    <option value="secondary" label="Secondary school graduate" />
                    <option value="tertiary" label="College/University/Bootcamp graduate" />
                </select>
            </div>

            <div className="form-group">
                <label htmlFor="educationStatus">Education Status</label>
                <select
                    id="educationStatus"
                    name="educationStatus"
                    value={educationStatus}
                    onChange={(e) => setEducationStatus(e.target.value)}
                    className="education_status"
                >
                    <option value="" label="Select education status" />
                    <option value="schooling" label="Schooling" />
                    <option value="graduated" label="Graduated" />
                    <option value="any" label="Any, I don't care!" />
                </select>
            </div>

            <button className="save-btn" onClick={handleSave}>Save</button>
        </div>
    );
};

export default PreferenceForm;
