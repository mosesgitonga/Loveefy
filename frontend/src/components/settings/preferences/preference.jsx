import React, { useEffect, useState } from "react";

const PreferenceSettings = () => {
    const [gender, setGender] = useState('')
    const [industry_major, setIndustry_major] = useState('')
    const [career, setCareer] = useState('')

    useEffect(() => {
        // Fetch the existing user profile
        const fetchProfile = async () => {
            try {
                const response = await api.get(`/api/v1/preferences`);
                const preferenceData = response.data;
                console.log(preferenceData)
                setGender(preferenceData.gender);
                setIndustry_major(preferenceData.industry);
                setCareer(preferenceData.career);
            } catch (error) {
                console.error('Error fetching profile data:', error.response?.data?.error || error.message);
            }
        };

        fetchProfile();
    }, []);

    const handleSave = async () => {
        try {
            const preferenceData = {
                username,
                industry_major,
                career,
                dob
            };

            const response = api.patch('/api/v1/preference', preferenceData);
            alert(response.data.message); // Display success message
        } catch (error) {
            alert('Error updating profile: ' + error.response?.data?.error || error.message);
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
            <button className="save-btn" onClick={handleSave}>Save</button>
        </div>
    );
}
export default PreferenceSettings;