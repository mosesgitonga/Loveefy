import React, { useState } from 'react';
import './feedback.css'; 
import api from './api/axios';

const FeedbackForm = () => {
    const [remarks, setRemarks] = useState('');
    const [suggestions, setSuggestions] = useState('');
    const [rating, setRating] = useState(0);
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await api.post('/api/v1/feedback', { remarks, suggestions, ratings: rating });

            if (response.status === 200) {
                setMessage(response.data.message);
                setRemarks('');
                setSuggestions('');
                setRating(0); // Reset to 0 instead of 1 for user feedback
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
            <div className="feedback-form">
                <h2>Feedback Form</h2>
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
                    <button type="submit">Submit Feedback</button>
                </form>
                {message && <p className="feedback-message">{message}</p>}
            </div>
        </div>
    );
};

export default FeedbackForm;
