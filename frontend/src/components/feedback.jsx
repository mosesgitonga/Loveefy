import React, { useState } from 'react';
import './feedback.css'; // Ensure this CSS file exists and is properly styled
import api from './api/axios'; // Make sure this is set up correctly for your POST requests

const FeedbackForm = () => {
    const [remarks, setRemarks] = useState('');
    const [suggestions, setSuggestions] = useState('');
    const [rating, setRating] = useState(0);
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Ensure you're sending a POST request with proper payload
            const response = await api.post('/api/v1/feedback', { remarks, suggestions, ratings: rating });

            // Directly use response.data if using axios
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
    );
};

export default FeedbackForm;
