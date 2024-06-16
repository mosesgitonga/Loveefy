import React, { useState } from "react";
import api from "../api/axios";
import { useNavigate } from 'react-router-dom'
import styles from './login.module.css'

const Login = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    })

    const [errorMessage, setErrorMessage] = useState('')

    const navigate = useNavigate()

    const handleSubmit = (e) => {
        e.preventDefault()
        
        
        api.post('v1/auth/logins')
            .then(response => {
                if (response.status_code === 200) {
                    navigate('/profile/setup')
                }
                setErrorMessage(response)
            })
            .catch(error => {
                console.log(error)
                setErrorMessage('Registration Failed. please Try Again')
            })
    }

    const handleChange = (e) => {
        const [name, value] = e.target()

        setFormData({
            ...formData,
            [name]:value
        })
    }

    return (
        <div className="loginPage" >
            <h2>Login</h2>
            <form onSubmit={handleSubmit} className={styles.form}>
                <div className={styles.formGroup}>
                    <label htmlFor="email">Eamil</label>
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
                <p><a href="#">Forgot password</a></p>
                <p>Don't have an account? <a href="/register">Register</a></p>
            </form>
        </div>
    )
}

export default Login;