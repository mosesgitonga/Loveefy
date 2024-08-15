import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import './Upload_pic.css';

const Upload = () => {
    const navigate = useNavigate();
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);

    // Function to handle file selection
    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        setFile(selectedFile);
    };

    // Function to handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!file) {
            alert("Please select a file to upload");
            return;
        }

        try {
            setLoading(true);
            const formData = new FormData();
            formData.append("file", file);

            const response = await api.post("/v1/pic/uploads", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });

            if (response.status === 200) {
                const data = response.data;
                setMessage("Image uploaded successfully");
                alert('image uploaded successfully')
                navigate("/discovery/home");
            } else {
                setMessage("Failed to upload image");
            }
        } catch (error) {
            if (error.response) {
                console.error("Error response:", error.response);
                setMessage(`Error: ${error.response.data.message || error.response.statusText}`);
            } else if (error.request) {
                console.error("Error request:", error.request);
                setMessage("No response from server.");
            } else {
                console.error("Error message:", error.message);
                setMessage("An error occurred while uploading image");
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-window">
            <div className="form">
                <form onSubmit={handleSubmit} encType="multipart/form-data">
                    <input type="file" name="file" id="file" onChange={handleFileChange} />
                    <label htmlFor="file">Choose a file</label>
                    {file && <p className="file-name">{file.name}</p>}
                    <button type="submit" disabled={loading}>
                        {loading ? "Uploading..." : "Upload"}
                    </button>
                </form>
                {message && <p>{message}</p>}
            </div>
        </div>
    );
};

export default Upload;
