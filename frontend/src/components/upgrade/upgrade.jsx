import React, { useState } from 'react';
import './upgrade.css'; 
import api from '../api/axios';

const GoldPackageSubscription = () => {
    const [phoneNumber, setPhoneNumber] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            const response = await api.post('https://www.loveefy.africa/api/mpesa/stk-push', {
                phone_number: phoneNumber,
                amount: 1,
                subscription_type: 'gold'
            });

            if (response.data.status === 'pending') {
                setMessage('Payment request sent! Please check your phone for the MPESA request.');
            } else {
                setMessage('Failed to initiate payment.');
            }
        } catch (error) {
            console.error(error);
            setMessage('An error occurred. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className='subscription-container'>
            <p>This Feature is Not Yet Available</p>
            <p>Enjoy all our features for now.</p>

        </div>
    )

    // return (
    //     <div className="subscription-container">
    //         <div className="subscription-card">
    //             <h2>🌟 Subscribe to the Gold Package 🌟</h2>
    //             <p className="subscription-description">
    //                 Enjoy exclusive benefits for just <strong>1 Ksh!</strong>
    //             </p>
    //             <p className="payment-method">
    //                 Payment Method: <strong>MPESA</strong>
    //             </p>
    //             <form onSubmit={handleSubmit}>
    //                 <div className="input-group">
    //                     <label htmlFor="phone-number">Phone Number:</label>
    //                     <input
    //                         type="text"
    //                         id="phone-number"
    //                         value={phoneNumber}
    //                         onChange={(e) => setPhoneNumber(e.target.value)}
    //                         required
    //                         placeholder="e.g. 2547XXXXXXXX"
    //                         className="input-field"
    //                     />
    //                 </div>
    //                 <button type="submit" className="subscribe-button" disabled={loading}>
    //                     {loading ? 'Processing...' : 'Subscribe Now!'}
    //                 </button>
    //             </form>
    //             {message && <p className={`response-message ${loading ? 'loading' : ''}`}>{message}</p>}
    //         </div>
    //     </div>
    // );
};

export default GoldPackageSubscription;
