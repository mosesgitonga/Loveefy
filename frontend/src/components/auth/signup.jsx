import React, { useState } from "react";
import api from "../api/axios";
import styles from './signup.module.css';
import { useNavigate } from 'react-router-dom';

const Signup = () => {
    const navigate = useNavigate();
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [errorMessage, setErrorMessage] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (formData.password !== formData.confirmPassword) {
            setErrorMessage('Passwords do not match');
            return;
        }
         
        api.post('/api/v1/auth/registers', formData)
            .then(response => {
                if (response.status === 409 && response.data.code === 600) {
                    setErrorMessage('email already exists')
                }
                if (response.status === 201) {
                    navigate('/login');
                }
                console.log(response);
            })
            .catch(error => {
                console.log(error);
                if (error.response?.data.code === 600) {
                    setErrorMessage("Couldn't register. Email already exists. Please login")
                } else if (error.response?.status === 500) {
                    setErrorMessage('Internal server error. The problem is our servers')
                }
                else {
                    setErrorMessage('Registration failed. Please try again.');
                }
            });
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
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
                    <label htmlFor="username">Username</label>
                    <input 
                        type="text" 
                        placeholder="johndoe23"
                        name="username" 
                        value={formData.username}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className={styles.formgroup}>
                    <label htmlFor="email">Email</label>
                    <input 
                        type="email"
                        name="email"
                        value={formData.email}
                        placeholder="johndoe@example.com"
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
                <button type="submit">Register</button>
                <p className={styles.accountAlready}>Already have an Account? <a href="#">Login</a></p>
            </form>
        </div>
    )
}

export default Signup;

