import React, { useState } from "react";
import api from "../api/axios";
import { useNavigate } from 'react-router-dom';
import styles from './login.module.css';
import axios from "axios";

axios.defaults.baseURL = 'http://localhost:5000';
axios.defaults.headers.common['Content-Type'] = 'application/json';

const Login = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });

    const [errorMessage, setErrorMessage] = useState('');

    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();

        api.post('v1/auth/logins', formData)
            .then(response => {
                if (response.status === 200) {
                    localStorage.setItem('access_token', response.data.access_token);
                    navigate('/profile/setup');
                } else {
                    setErrorMessage(response.data.error || 'Login failed. Please try again.');
                }
            })
            .catch(error => {
                console.log(error);
                if (error.response?.status === 403) {
                    setErrorMessage('Forbidden Email or Password. Try again');
                } else {
                    setErrorMessage(error.response?.data?.error || 'Login failed. Please try again.');
                }
            });
    };

    const handleChange = (e) => {
        const { name, value } = e.target;

        setFormData({
            ...formData,
            [name]: value
        });
    };

    return (
        <div className={styles.loginWindow}>
            <div className={styles.loginContainer}>
                <h2>Login</h2>
                <form onSubmit={handleSubmit} className={styles.form}>
                    <div className={styles.formGroup}>
                        <label htmlFor="email">Email</label>
                        <input type="email"
                            placeholder="johndoe@example.com"
                            autoComplete="on"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <div className={styles.formGroup}>
                        <label htmlFor="password">Password</label>
                        <input type="password"
                            placeholder=""
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            required
                        />
                    </div>
                    <button type="submit">Submit</button>
                    <p><a href="#">Forgot password</a></p>
                    <p>Don't have an account? <a href="/register">Register</a></p>
                    {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
                </form>
            </div>
        </div>
    );
};

export default Login;
