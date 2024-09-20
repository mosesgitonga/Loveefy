import React, { useState } from "react";
import DeleteAccount from "./delete_acc";

const AccountSettings = () => {
    const [showConfirm, setShowConfirm] = useState(false);
    const [showDeleteForm, setShowDeleteForm] = useState(false);

    const handleDeleteClick = () => {
        setShowConfirm(true);
    };

    const confirmDelete = () => {
        setShowDeleteForm(true);
        setShowConfirm(false);
    };

    const cancelDelete = () => {
        setShowConfirm(false);
    };

    return (
        <div>
            <h2>Account Settings</h2>
            <button onClick={handleDeleteClick}>Delete Account</button>

            {showConfirm && (
                <div>
                    <p>Are you sure you want to delete your account?</p>
                    <button onClick={confirmDelete}>Yes, Delete</button>
                    <button onClick={cancelDelete}>Cancel</button>
                </div>
            )}

            {showDeleteForm && <DeleteAccount />}
        </div>
    );
};

export default AccountSettings;
