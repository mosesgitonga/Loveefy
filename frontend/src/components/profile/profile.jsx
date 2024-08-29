import React from "react";
import styles from './profile.module.css';
import * as yup from 'yup';
import { useFormik } from 'formik';
import api from '../api/axios'; 
import { useNavigate } from 'react-router-dom';

// Validation schema using Yup
const validationSchema = yup.object({
    gender: yup.string().required("Gender is required"),
    dob: yup.string().required("Date of birth is required"),
    mobile_no: yup.string()
        .required("Mobile number is required")
        .matches(/^[0-9]{10}$/, "Mobile number must be exactly 10 digits"),
    industry_major: yup.string(),
    education_level: yup.string().required("Education level is required"),
    career: yup.string().required("Career is required"),
    employment: yup.string().required("Employment is required"),
    is_schooling: yup.string().required("is schooling field is required"),

    has_child: yup.string().required("This field is required"),
    wants_child: yup.string(),
    country: yup.string().required("Country is required"),
    region: yup.string().required("Region is required"),
    sub_region: yup.string()
});

const Profile = () => {
    const navigate = useNavigate();

    const formik = useFormik({
        initialValues: {
            gender: '',
            dob: '',
            mobile_no: '',
            industry_major: '',
            education_level: '',
            employment: '',
            is_schooling: '',
            career: '',
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
                const response = await api.post('/api/v1/profiles', values);

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
                    <div className={styles.row}>
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
                        <label htmlFor="dob">
                            Date of Birth:
                            <input
                                id="dob"
                                type="date"
                                name="dob"
                                value={formik.values.dob}
                                onChange={formik.handleChange}
                                style={{ width: "100%" }} // Make the width responsive
                                inputmode="numeric" // Helps mobile devices understand the input type
                            />
                            {formik.errors.dob && <div className={styles.error}>{formik.errors.dob}</div>}
                        </label>
                        <label htmlFor="mobile_no">
                            Mobile Number (will not be shared):
                            <input
                                id="mobile_no"
                                type="text"
                                name="mobile_no"
                                value={formik.values.mobile_no}
                                onChange={formik.handleChange}
                                style={{width: "250px"}}
                            />
                            {formik.errors.mobile_no && <div className={styles.error}>{formik.errors.mobile_no}</div>}
                        </label>
                    </div>
                    <div className={styles.row}>
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
                                <option value="it" label="IT" />
                                <option value="finance" label="Finance" />
                                <option value="business" label="Business" />
                                <option value="law" label="Law" />
                                <option value="engineering" label="Engineering" />
                                <option value="education" label="Education" />
                                <option value="scientific_research" label="Scientific Research" />
                                <option value="manufacturing" label="Manufacturing" />
                                <option value="retail" label="Retail" />
                                <option value="fashion" label="fashion" />

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
                        <label htmlFor="education_level">
                            Education Level:
                            <input
                                id="education_level"
                                type="text"
                                name="education_level"
                                value={formik.values.education_level}
                                onChange={formik.handleChange}
                                style={{width: "250px"}}
                            />
                            {formik.errors.education_level && <div className={styles.error}>{formik.errors.education_level}</div>}
                        </label>
                        <label htmlFor="career">
                            Career:
                            <input
                                id="career"
                                type="text"
                                name="career"
                                value={formik.values.career}
                                onChange={formik.handleChange}
                                style={{width: "250px"}}
                            />
                            {formik.errors.career && <div className={styles.error}>{formik.errors.career}</div>}
                        </label>
                    </div>
                    <div className={styles.row}>
                        <label htmlFor="employment">
                            Employment:
                            <select
                                id="employment"
                                name="employment"
                                value={formik.values.employment}
                                onChange={formik.handleChange}
                                className={styles.employment}
                            >
                                <option value="">I am: </option>
                                <option value="employed">--Employed</option>
                                <option value="unemployed">--Unemployed</option>
                                <option value="self-employed">--Self Employed</option>
                                <option value="entrepreneur">--entrepreneur</option>
                            </select>
                            {formik.errors.employment && <div className={styles.error}>{formik.errors.employment}</div>}
                        </label>
                        <label htmlFor="is_schooling">
                            Are you Schooling?:
                            <select
                                id="is_schooling"
                                name="is_schooling"
                                value={formik.values.employment}
                                onChange={formik.handleChange}
                                className={styles.employment}
                            >
                                <option value="">Are you schooling: </option>
                                <option value="yes">Yes, i am schooling.</option>
                                <option value="no">No, I am done with school</option>
                            </select>
                            {formik.errors.is_schooling && <div className={styles.error}>{formik.errors.is_schooling}</div>}
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
                    </div>
                    <div className={styles.row}>
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
                                style={{width: "250px"}}
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
                                style={{width: "250px"}}
                            />
                            {formik.errors.region && <div className={styles.error}>{formik.errors.region}</div>}
                        </label>
                    </div>
                    <div className={styles.row}>
                        <label htmlFor="sub_region">
                            Sub Region:
                            <input
                                id="sub_region"
                                type="text"
                                name="sub_region"
                                value={formik.values.sub_region}
                                onChange={formik.handleChange}
                                style={{width: "250px"}}
                            />
                            {formik.errors.sub_region && <div className={styles.error}>{formik.errors.sub_region}</div>}
                        </label>
                    </div>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </div>
    );
};

export default Profile;
