import React, { useState } from "react";
import api from "../api/axios";
import { useNavigate } from 'react-router-dom';
import styles from './login.module.css';
import { Link } from 'react-router-dom'
import axios from "axios";


const Login = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    });

    
    const [errorMessage, setErrorMessage] = useState('');

    const navigate = useNavigate()

    const handleSubmit = (e) => {
        e.preventDefault();

        api.post('v1/auth/logins', formData)
            .then(response => {
                if (response.status === 200) {
                    const { current_username, current_user_id ,access_token, place_id, preference_id } = response.data;
                    sessionStorage.setItem('access_token', access_token);
                    sessionStorage.setItem('userId', current_user_id);
                    sessionStorage.setItem('currentUsername', current_username);
                    if (place_id && preference_id) {
                        navigate('/discovery/home');
                    } else if (place_id && !preference_id) {
                        navigate('/preference');
                    } else {
                        navigate('/profile/setup'); // Default redirection if neither is set
                    }
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
                    <p><Link to="/forgot-password">Forgot password</Link></p>
                    <p>Don't have an account? <Link to="/register">Register</Link></p>
                    {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}
                </form>
            </div>
        </div>
    );
};

export default Login;
