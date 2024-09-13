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
    const [gender, setGender] = useState('');
    const [mobileNo, setMobileNo] = useState('');
    const [industryMajor, setIndustryMajor] = useState('');
    const [educationLevel, setEducationLevel] = useState('');
    const [employment, setEmployment] = useState('');
    const [isSchooling, setIsSchooling] = useState('');
    const [hasChild, setHasChild] = useState('');
    const [wantsChild, setWantsChild] = useState('');

    useEffect(() => {
        // Fetch the existing user profile
        const fetchProfile = async () => {
            const userId = sessionStorage.getItem('userId');
            try {
                const response = await api.get(`/api/v1/profile/${userId}`);
                const profileData = response.data;
                console.log(profileData);
                setUsername(profileData.message.username);
                setIndustry(profileData.message.industry);
                setCareer(profileData.message.career);
                setDob(profileData.message.dob);
                setGender(profileData.message.gender || '');
                setMobileNo(profileData.message.mobile_no);
                setIndustryMajor(profileData.message.industry_major || '');
                setEducationLevel(profileData.message.education_level || '');
                setEmployment(profileData.message.employment || '');
                setIsSchooling(profileData.message.is_schooling || '');
                setHasChild(profileData.message.has_child || '');
                setWantsChild(profileData.message.wants_child || '');
                setCountry(profileData.message.country || '');
                setRegion(profileData.message.region || '');
                setSubRegion(profileData.message.sub_region || '');
                console.log('data mobile', profileData.message.mobile_no)
                console.log('mobile no', mobileNo)
            } catch (error) {
                console.error('Error fetching profile data:', error.response?.data?.error || error.message);
            }
        };

        fetchProfile();
    }, [userId]);

    const handleSave = async (e) => {
        e.preventDefault();
        try {
            const profileData = {
                username,
                industry,
                career,
                dob,
                gender,
                mobile_no: mobileNo,
                industry_major: industryMajor,
                education_level: educationLevel,
                employment,
                is_schooling: isSchooling,
                has_child: hasChild,
                wants_child: wantsChild,
                country,
                region,
                sub_region: subRegion,
            };

            const response = await api.patch('/api/v1/profiles/update', profileData);
            alert(response.data.message); // Display success message
        } catch (error) {
            alert('Error updating profile: ' + (error.response?.data?.error || error.message));
        }
    };

    return (
        <div className="profileWindow">
            <h1>Loveefy</h1>
            <div className="profileContainer">
                <h2>Profile Update Setting</h2>
                <form onSubmit={handleSave} className="form">
                    <div className="row">
                        <label htmlFor="gender">
                            Gender:
                            <select
                                id="gender"
                                name="gender"
                                value={gender ||"gender"}
                                onChange={(e) => setGender(e.target.value)}
                                className="gender"
                            >
                                <option value="" label="Select gender" />
                                <option value="male" label="Male" />
                                <option value="female" label="Female" />
                            </select>
                        </label>
                        <label htmlFor="dob">
                            Date of Birth:
                            <input
                                id="dob"
                                type="date"
                                name="dob"
                                value={dob || "dob"}
                                onChange={(e) => setDob(e.target.value)}
                                style={{ width: '100%' }} // Make the width responsive
                            />
                        </label>
                        <label htmlFor="mobile_no">
                            Mobile Number (will not be shared):
                            <input
                                id="mobile_no"
                                type="text"
                                name="mobile_no"
                                value={mobileNo || "mobile_no"}
                                onChange={(e) => setMobileNo(e.target.value)}
                                style={{ width: '250px' }}
                            />
                        </label>
                    </div>
                    <div className="row">
                        <label htmlFor="industry_major">
                            Industry Major:
                            <select
                                id="industry_major"
                                name="industry_major"
                                value={industryMajor || "industry"}
                                onChange={(e) => setIndustryMajor(e.target.value)}
                                className="industryMajor"
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
                                <option value="fashion" label="Fashion" />
                                <option value="transportation" label="Transportation" />
                                <option value="agriculture" label="Agriculture" />
                                <option value="hospitality" label="Hospitality" />
                                <option value="construction" label="Construction" />
                                <option value="real_estate" label="Real Estate" />
                                <option value="security" label="Security" />
                                <option value="others" label="Others" />
                            </select>
                        </label>
                        <label htmlFor="education_level">
                            Education Level:
                            <input
                                id="education_level"
                                type="text"
                                name="education_level"
                                value={educationLevel || "education"}
                                onChange={(e) => setEducationLevel(e.target.value)}
                                style={{ width: '250px' }}
                            />
                        </label>
                        <label htmlFor="career">
                            Career:
                            <input
                                id="career"
                                type="text"
                                name="career"
                                value={career || "career"}
                                onChange={(e) => setCareer(e.target.value)}
                                style={{ width: '250px' }}
                            />
                        </label>
                    </div>
                    <div className="row">
                        <label htmlFor="employment">
                            Employment:
                            <select
                                id="employment"
                                name="employment"
                                value={employment || "employment"}
                                onChange={(e) => setEmployment(e.target.value)}
                                className="employment"
                            >
                                <option value="">I am: </option>
                                <option value="employed">--Employed</option>
                                <option value="unemployed">--Unemployed</option>
                                <option value="self-employed">--Self Employed</option>
                                <option value="entrepreneur">--Entrepreneur</option>
                            </select>
                        </label>
                        <label htmlFor="is_schooling">
                            Are you Schooling?:
                            <select
                                id="is_schooling"
                                name="is_schooling"
                                value={isSchooling || "schooling"}
                                onChange={(e) => setIsSchooling(e.target.value)}
                                className="employment"
                            >
                                <option value="">Are you schooling: </option>
                                <option value="yes">Yes, I am schooling.</option>
                                <option value="no">No, I am done with school</option>
                            </select>
                        </label>
                        <label htmlFor="has_child">
                            Has Child:
                            <select
                                id="has_child"
                                name="has_child"
                                value={hasChild || "has child"}
                                onChange={(e) => setHasChild(e.target.value)}
                                className="has_child"
                            >
                                <option value="" label="Do you have a child?" />
                                <option value="no" label="No, I don't have" />
                                <option value="yes" label="Yes, I have" />
                            </select>
                        </label>
                    </div>
                    <div className="row">
                        <label htmlFor="wants_child">
                            Wants Child:
                            <select
                                id="wants_child"
                                name="wants_child"
                                value={wantsChild || "wants child"}
                                onChange={(e) => setWantsChild(e.target.value)}
                                className="wants_child"
                            >
                                <option value="" label="Do you want to have a child?" />
                                <option value="no" label="No, I don't" />
                                <option value="yes" label="Yes, I want to" />
                                <option value="soon" label="Not now, but soon" />
                            </select>
                        </label>
                        <label htmlFor="country">
                            Country:
                            <input
                                id="country"
                                type="text"
                                name="country"
                                value={country || "country"}
                                onChange={(e) => setCountry(e.target.value)}
                                style={{ width: '250px' }}
                            />
                        </label>
                        <label htmlFor="region">
                            Region/State/County:
                            <input
                                id="region"
                                type="text"
                                name="region"
                                value={region || "region"}
                                onChange={(e) => setRegion(e.target.value)}
                                style={{ width: '250px' }}
                            />
                        </label>
                        <label htmlFor="sub_region">
                            Sub-Region:
                            <input
                                id="sub_region"
                                type="text"
                                name="sub_region"
                                value={subRegion || "subregion"}
                                onChange={(e) => setSubRegion(e.target.value)}
                                style={{ width: '250px' }}
                            />
                        </label>
                    </div>
                    <button type="submit" className="submit-btn">Save Profile</button>
                </form>
            </div>
        </div>
    );
};

export default ProfileSettings;
