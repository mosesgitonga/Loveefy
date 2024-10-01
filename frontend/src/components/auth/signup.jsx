import React, { useState } from "react";
import api from "../api/axios";
import styles from './signup.module.css';
import { useNavigate, Link } from 'react-router-dom';

const Signup = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [errorMessage, setErrorMessage] = useState('');
    const [usernameValidationMessage, setUsernameValidationMessage] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();

        if (formData.password !== formData.confirmPassword) {
            setErrorMessage('Passwords do not match');
            return;
        }

        // Validate that username is not an email
        if (usernameValidationMessage) {
            setErrorMessage('Please choose a valid username');
            return;
        }

        setIsSubmitting(true); 

        api.post('/api/v1/auth/registers', formData)
            .then(response => {
                setIsSubmitting(false); 
                if (response.status === 409 && response.data.code === 600) {
                    setErrorMessage('Email already exists');
                }
                if (response.status === 201) {
                    navigate('/login');
                }
                console.log(response);
            })
            .catch(error => {
                setIsSubmitting(false); 
                console.log(error);
                if (error.response?.data.code === 600) {
                    setErrorMessage("Couldn't register. Email already exists. Please login");
                } else if (error.response?.status === 500) {
                    setErrorMessage('Internal server error. The problem is on our servers.');
                } else {
                    setErrorMessage('Registration failed. Please try again.');
                }
            });
    }

    const handleChange = (e) => {
        const { name, value } = e.target;

        // Check if the entered username contains an '@' symbol to prevent email as username
        if (name === "username" && value.includes('@')) {
            setUsernameValidationMessage("Username cannot contain an email address");
        } else {
            setUsernameValidationMessage('');
        }

        setFormData({
            ...formData,
            [name]: value
        });
    }

    return (
        <div className={styles.signupContainer}>
            <h2>Register</h2>
            <form onSubmit={handleSubmit} className={styles.form} autoComplete="off">
                {errorMessage && <p className={styles.error}>{errorMessage}</p>}

                <div className={styles.formgroup}>
                    <label htmlFor="email">Email</label>
                    <input 
                        type="email"
                        name="email"
                        value={formData.email}
                        placeholder="johndoe@example.com"
                        autoComplete="email"
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className={styles.formgroup}>
                    <label htmlFor="password">Password</label>
                    <input 
                        type="password" 
                        name="password"
                        value={formData.password}
                        onChange={handleChange} 
                        required
                    />
                </div>
                <div className={styles.formgroup}>
                    <label htmlFor="confirmPassword">Confirm Password</label>
                    <input 
                        type="password" 
                        name="confirmPassword"
                        value={formData.confirmPassword}
                        onChange={handleChange} 
                        required
                    />
                </div>
                <div className={styles.formgroup}>
                    <label htmlFor="username">YOUR NAME</label>
                    <input 
                        type="text" 
                        placeholder="johndoe23"
                        name="username" 
                        value={formData.username}
                        autoComplete="off"
                        onChange={handleChange}
                        required
                    />
                    {/* Display the validation message if the username contains an email pattern */}
                    {usernameValidationMessage && <p className={styles.error}>{usernameValidationMessage}</p>}
                </div>

                <button type="submit" disabled={isSubmitting}>
                    {isSubmitting ? 'Submitting...' : 'Register'}
                </button>
                <p className={styles.accountAlready}>Already have an Account? <Link to="/login">Login</Link></p>
            </form>
        </div>
    )
}

export default Signup;
