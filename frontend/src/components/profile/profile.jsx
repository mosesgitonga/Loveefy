// Profile.jsx

import React from "react";
import styles from './profile.module.css';
import * as yup from 'yup';
import { useFormik } from 'formik';
import api from '../api/axios'; 
import { useNavigate } from 'react-router-dom';

// Validation schema using Yup
const validationSchema = yup.object({
    gender: yup.string().required("Gender is required"),
    age: yup.number().required("Age is required").min(18, "You must be at least 18 years old"),
    mobile_no: yup.string()
        .required("Mobile number is required")
        .matches(/^[0-9]{10}$/, "Mobile number must be exactly 10 digits"),
    subscription_type: yup.string().required("Subscription type is required"),
    industry_major: yup.string().required("Industry major is required"),
    fav_hobby: yup.string().required("Favorite hobby is required"),
    has_child: yup.string().required("This field is required"),
    wants_child: yup.string().required("This field is required"),
    country: yup.string().required("Country is required"),
    region: yup.string().required("Region is required"),
    sub_region: yup.string()
});

const Profile = () => {
    const navigate = useNavigate();

    const formik = useFormik({
        initialValues: {
            gender: '',
            age: '',
            mobile_no: '',
            subscription_type: '',
            industry_major: '',
            fav_hobby: '',
            has_child: '',
            wants_child: '',
            country: '',
            region: '',
            sub_region: ''
        },
        validationSchema: validationSchema,
        onSubmit: async values => {
            console.log(JSON.stringify(values, null, 2));
            try {
                const response = await api.post('/v1/profiles', values);

                if (response.status === 201) {
                    console.log('Profile created successfully');
                    navigate('/preference');
                } else {
                    console.log('Unexpected status code:', response.status);
                }
            } catch (error) {
                console.error('Error creating profile:', error);
                if (error.response) {
                    console.log('Error response data:', error.response.data);
                    console.log('Error response status:', error.response.status);
                    console.log('Error response headers:', error.response.headers);
                } else if (error.request) {
                    console.log('Request data:', error.request);
                } else {
                    console.log('Error message:', error.message);
                }
                console.log('Error config:', error.config);
            }
        }
    });

    return (
        <div className={styles.profileWindow}>
            <h1>Loveefy</h1>
            <div className={styles.profileContainer}>
                <h2>Profile Setup</h2>
                <form onSubmit={formik.handleSubmit} className={styles.form}>
                    <label htmlFor="gender">
                        Gender:
                        <select
                            id="gender"
                            name="gender"
                            value={formik.values.gender}
                            onChange={formik.handleChange}
                            className={styles.gender}
                        >
                            <option value="" label="Select gender" />
                            <option value="male" label="Male" />
                            <option value="female" label="Female" />
                        </select>
                        {formik.errors.gender && <div className={styles.error}>{formik.errors.gender}</div>}
                    </label>
                    <label htmlFor="age">
                        Age:
                        <input
                            id="age"
                            type="number"
                            name="age"
                            value={formik.values.age}
                            onChange={formik.handleChange}
                        />
                        {formik.errors.age && <div className={styles.error}>{formik.errors.age}</div>}
                    </label>
                    <label htmlFor="mobile_no">
                        Mobile Number (will not be shared):
                        <input
                            id="mobile_no"
                            type="text"
                            name="mobile_no"
                            value={formik.values.mobile_no}
                            onChange={formik.handleChange}
                        />
                        {formik.errors.mobile_no && <div className={styles.error}>{formik.errors.mobile_no}</div>}
                    </label>
                    <label htmlFor="subscription_type">
                        Subscription Type:
                        <select
                            id="subscription_type"
                            name="subscription_type"
                            value={formik.values.subscription_type}
                            onChange={formik.handleChange}
                        >
                            <option value="" label="Select subscription type" />
                            <option value="free" label="Free" />
                            <option value="gold" label="Gold" />
                            <option value="elite" label="Elite" />
                        </select>
                        {formik.errors.subscription_type && <div className={styles.error}>{formik.errors.subscription_type}</div>}
                    </label>
                    <label htmlFor="industry_major">
                        Industry Major:
                        <select
                            id="industry_major"
                            name="industry_major"
                            value={formik.values.industry_major}
                            onChange={formik.handleChange}
                            className={styles.industryMajor}
                        >
                            <option value="" label="Select industry major" />
                            <option value="health" label="Health" />
                            <option value="Information TechnologyT" label="Information Technology" />
                            <option value="finance" label="Finance" />
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
                        {formik.errors.industry_major && <div className={styles.error}>{formik.errors.industry_major}</div>}
                    </label>
                    <label htmlFor="fav_hobby">
                        Favorite Hobby:
                        <input
                            id="fav_hobby"
                            type="text"
                            name="fav_hobby"
                            value={formik.values.fav_hobby}
                            onChange={formik.handleChange}
                        />
                        {formik.errors.fav_hobby && <div className={styles.error}>{formik.errors.fav_hobby}</div>}
                    </label>
                    <label htmlFor="has_child">
                        Has Child:
                        <select
                            id="has_child"
                            name="has_child"
                            value={formik.values.has_child}
                            onChange={formik.handleChange}
                            className={styles.has_child}
                        >
                            <option value="" label="Do you have a child?" />
                            <option value="no" label="No, I don't have" />
                            <option value="yes" label="Yes, I have" />
                        </select>
                        {formik.errors.has_child && <div className={styles.error}>{formik.errors.has_child}</div>}
                    </label>
                    <label htmlFor="wants_child">
                        Wants Child:
                        <select
                            id="wants_child"
                            name="wants_child"
                            value={formik.values.wants_child}
                            onChange={formik.handleChange}
                            className={styles.wants_child}
                        >
                            <option value="" label="Do you want to have a child?" />
                            <option value="no" label="No, I don't" />
                            <option value="yes" label="Yes, I want to" />
                            <option value="soon" label="Not now, but soon" />
                        </select>
                        {formik.errors.wants_child && <div className={styles.error}>{formik.errors.wants_child}</div>}
                    </label>
                    <label htmlFor="country">
                        Country:
                        <input
                            id="country"
                            type="text"
                            name="country"
                            value={formik.values.country}
                            onChange={formik.handleChange}
                        />
                        {formik.errors.country && <div className={styles.error}>{formik.errors.country}</div>}
                    </label>
                    <label htmlFor="region">
                        Region/State/County:
                        <input
                            id="region"
                            type="text"
                            name="region"
                            value={formik.values.region}
                            onChange={formik.handleChange}
                        />
                        {formik.errors.region && <div className={styles.error}>{formik.errors.region}</div>}
                    </label>
                    <label htmlFor="sub_region">
                        Sub Region:
                        <input
                            id="sub_region"
                            type="text"
                            name="sub_region"
                            value={formik.values.sub_region}
                            onChange={formik.handleChange}
                        />
                        {formik.errors.sub_region && <div className={styles.error}>{formik.errors.sub_region}</div>}
                    </label>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
};

export default Profile;
