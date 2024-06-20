import React from "react";
import styles from './profile.module.css';
import * as yup from 'yup';
import { useFormik, validateYupSchema } from 'formik';
import api from '../api/axios.jsx'

const validationSchema = yup.object({
    age: yup.number().required("Age is required").min(18, "18 and above - Kids are not allowed, Go play video games"),
    mobile_no: yup.string()
        .required("Mobile number is required")
        .matches(/^[0-9]{10}$/, "Mobile number must be 10 digits"),
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
                    const response = await api.post('/v1/profiles', values)  

                    if (response === 201) {
                        console.log('profile created successfully')

                    } else {
                        console.log('unexpected status code')
                    }
                } catch(error) {
                    console.log('Error creating profile')
                    if (error.response) {
                        console.log(error.response.data)
                        console.log(error.response.status)
                        console.log(error.response.headers)
                    }
                    else if (error.request) {
                        console.log('Request data:', error.request)
                    } else {
                        console.log(error.message)
                    }
                    console.log('Error config', error.config)
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
                        Mobile Number(will not be shared):
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
                            type="text"
                            name="subscription_type"
                            value={formik.values.subscription_type}
                            onChange={formik.handleChange}
                        >
                            <option value="">Select subscription type</option>
                            <option value="free">Free</option>
                            <option value="gold">Gold</option>
                            <option value="elite">Elite</option>
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
                            <option value="" label="Which industry are you in?" />
                            <option value="health" label="Health" />
                            <option value="it" label="IT" />
                            <option value="finance" label="Finance" />
                            <option value="law" label="Law" />
                            <option value="engineering" label="Engineering"/>
                            <option value="education" label="Education" />
                            <option value="scientific_research" label="Scientific research" />
                            <option value="manufacturing" label="Manufacturing" />
                            <option value="retail" label="Retail" />
                            <option value="transportation" label="Transportation" />
                            <option value="agriculture" label="Agriculture"/>
                            <option value="hospitality" label="Hospitality" />
                            <option value="construction" label="Construction" />
                            <option value="real_estate" label="Real Estate" />
                            <option value="security" label="security"/>

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
                            <option value="no" label="No, i don't have" />
                            <option value="yes" label="Yes i have" />
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
                            <option value="yes" label="Yes I want to" />
                            <option value="soom" label="Not now, Very soon" />
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
