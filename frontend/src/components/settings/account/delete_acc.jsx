import React, { useState } from "react";
import api from "../../api/axios";
import { useNavigate } from 'react-router-dom';


const DeleteAccount = () => {
    const [remarks, setRemarks] = useState('');
    const [suggestions, setSuggestions] = useState('');
    const [rating, setRating] = useState(0);
    const [message, setMessage] = useState('');
    const navigate = useNavigate()

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Sending feedback
            const feedbackResponse = await api.post('/api/v1/feedback', { remarks, suggestions, ratings: rating });

            if (feedbackResponse.status === 200) {
                setMessage(feedbackResponse.data.message);

                // Deleting the account
                const deleteResponse = await api.delete('/apidiscovery/notificationsdiscovery/notifications/v1/auth/account/delete');
                if (deleteResponse.status === 200) {
                    setMessage(deleteResponse.data.message);
                    sessionStorage.setItem('access_token', '');
                    navigate('/')
                }
                // Reset the form fields
                setRemarks('');
                setSuggestions('');
                setRating(0); 
            } else {
                setMessage('Error submitting feedback. Please try again.');
            }
        } catch (error) {
            console.error('Error submitting feedback:', error); // Log error for debugging
            setMessage('Error submitting feedback. Please try again.');
        }
    };

    const handleRatingClick = (value) => {
        setRating(value);
    };

    return (
        <div className='feedbackPage'>
            <h2>Feedback Form</h2>

            <h3>So Sad. Tell Us Why You Want To Leave Us, So That We Can Improve</h3>

            <div className="feedback-form">
                <form onSubmit={handleSubmit}>
                    <div className="form-group">
                        <label htmlFor="remarks">Remarks:</label>
                        <textarea
                            id="remarks"
                            value={remarks}
                            onChange={(e) => setRemarks(e.target.value)}
                            placeholder="Enter your remarks"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label htmlFor="suggestions">Suggestions:</label>
                        <textarea
                            id="suggestions"
                            value={suggestions}
                            onChange={(e) => setSuggestions(e.target.value)}
                            placeholder="Enter your suggestions"
                            required
                        />
                    </div>
                    <div className="form-group">
                        <label>Rating:</label>
                        <div className="rating">
                            {[1, 2, 3, 4, 5].map((value) => (
                                <span
                                    key={value}
                                    className={`star ${value <= rating ? 'filled' : ''}`}
                                    onClick={() => handleRatingClick(value)}
                                >
                                    ★
                                </span>
                            ))}
                        </div>
                    </div>
                    <button type="submit">Submit Feedback and Delete Account</button>
                </form>
                {message && <p className="feedback-message">{message}</p>}
            </div>
        </div>
    );
}

export default DeleteAccount;
