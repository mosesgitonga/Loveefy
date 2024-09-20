import React from "react";
import api from "../../api/axios";

const [remarks, setRemarks] = useState('');
const [suggestions, setSuggestions] = useState('');
const [rating, setRating] = useState(0);
const [message, setMessage] = useState('');

const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        // Ensure you're sending a POST request with proper payload
        const response = await api.post('/api/v1/feedback', { remarks, suggestions, ratings: rating });

        if (response.status === 200) {
            setMessage(response.data.message);
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

const DeleteAccount = () => {
    return (
        <div className='feedbackPage'>
            <h1>So Sad. Tell Us Why You Want To leave Us, So That We Can Improve</h1>
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
                    <button type="submit">Submit Feedback and Delete Account</button>
                </form>
            {message && <p className="feedback-message">{message}</p>}
        </div>
    </div>
    );
}