import React, { useState } from "react";
import api from "../api/axios";
import "./forgotPassword.css";

const ForgotPassword = () => {
    const [email, setEmail] = useState('');  
    const [message, setMessage] = useState('');
    const [showOTPForm, setShowOTPForm] = useState(false);
    const [otp, setOtp] = useState('');
    const [newPassword, setNewPassword] = useState('');

    const handleSubmitEmail = async (e) => {
        e.preventDefault();  

        try {
            const response = await api.post('/v1/auth/reset_password_request', { email });

            if (response.status === 200) {
                setMessage(response.data.message);
                setShowOTPForm(true);  // Show the OTP form
            } else {
                setMessage('Something went wrong. Please try again.');
            }
        } catch (error) {
            setMessage('An error occurred. Please try again later.');
        }
    };

    const handleOTPSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/api/v1/auth/update_password', { email, otp, newPassword });

            if (response.status === 200) {
                setMessage(response.data.message);
                // Optionally reset the form or redirect the user
            } else {
                setMessage('Failed to update password. Please try again.');
            }
        } catch (error) {
            setMessage(error.response?.data?.error || 'An error occurred. Please try again later.');
        }
    };

    return (
        <div className="forgot-password-container">
            {!showOTPForm ? (
                <form className="forgot-password-form" onSubmit={handleSubmitEmail}>
                    <label className="forgot-password-label" htmlFor="email">
                        Email:
                        <input 
                            type="email" 
                            className="forgot-password-input"
                            placeholder="johndoe@example.com" 
                            value={email} 
                            onChange={(e) => setEmail(e.target.value)}  
                            required
                        />
                    </label>
                    <button type="submit" className="forgot-password-button">Submit</button>
                    <p className="forgot-password-message">{message}</p>
                </form>
            ) : (
                <div className="otp-form">
                    <h2 className="forgot-password-heading">We have sent an OTP (one-time password) to your email</h2>
                    <h3 className="forgot-password-subheading">Enter OTP and New Password</h3>
                    <form className="forgot-password-form" onSubmit={handleOTPSubmit}>
                        <label className="forgot-password-label" htmlFor="otp">
                            OTP:
                            <input 
                                type="text" 
                                className="forgot-password-input" 
                                placeholder="Enter OTP" 
                                value={otp}
                                onChange={(e) => setOtp(e.target.value)}
                                required 
                            />
                        </label>
                        <label className="forgot-password-label" htmlFor="newPassword">
                            New Password:
                            <input 
                                type="password" 
                                className="forgot-password-input" 
                                placeholder="Enter New Password" 
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                required 
                            />
                        </label>
                        <button type="submit" className="forgot-password-button">Submit</button>
                        <p className="forgot-password-message">{message}</p>
                    </form>
                </div>
            )}
        </div>
    );
};

export default ForgotPassword;
