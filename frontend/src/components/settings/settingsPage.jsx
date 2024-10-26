import React, { useState, useEffect, useRef } from 'react';
import './settingsPage.css'; 
import ProfileSettings from './profile';
import PreferenceForm from './preferences/preference';
import AccountSettings from './account/account';

const SettingsPage = () => {
    const [activeTab, setActiveTab] = useState('profile');
    const [sidebarOpen, setSidebarOpen] = useState(false); // State for toggling sidebar
    const sidebarRef = useRef(null); // To reference the sidebar for click detection

    const handleTabChange = (tab) => {
        setActiveTab(tab);
        setSidebarOpen(false); // Close sidebar after selecting a tab
    };

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    // Handle clicking outside the sidebar
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (sidebarRef.current && !sidebarRef.current.contains(event.target)) {
                setSidebarOpen(false); // Close the sidebar if click happens outside
            }
        };

        if (sidebarOpen) {
            document.addEventListener('mousedown', handleClickOutside); // Add event listener when sidebar is open
        } else {
            document.removeEventListener('mousedown', handleClickOutside); // Remove event listener when sidebar is closed
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside); // Cleanup on component unmount
        };
    }, [sidebarOpen]);

    return (
        <div className="settings-page">
            <button className="hamburger" onClick={toggleSidebar}>
                &#9776;
            </button>
            <aside ref={sidebarRef} className={`settings-sidebar ${sidebarOpen ? 'open' : ''}`}>
                <h2>Settings</h2>
                <ul>
                    <li className={activeTab === 'profile' ? 'active' : ''} onClick={() => handleTabChange('profile')}>Profile</li>
                    <li className={activeTab === 'preference' ? 'active' : ''} onClick={() => handleTabChange('preference')}>Preference</li>
                    <li className={activeTab === 'account' ? 'active' : ''} onClick={() => handleTabChange('account')}>Account</li>
                    <li className={activeTab === 'security' ? 'active' : ''} onClick={() => handleTabChange('security')}>Security</li>
                    <li className={activeTab === 'interaction' ? 'active' : ''} onClick={() => handleTabChange('interaction')}>Interaction</li>
                    <li className={activeTab === 'content' ? 'active' : ''} onClick={() => handleTabChange('content')}>Content</li>
                    <li className={activeTab === 'accessibility' ? 'active' : ''} onClick={() => handleTabChange('accessibility')}>Accessibility</li>
                    <li className={activeTab === 'location' ? 'active' : ''} onClick={() => handleTabChange('location')}>Location</li>
                    <li className={activeTab === 'community' ? 'active' : ''} onClick={() => handleTabChange('community')}>Community</li>
                    <li className={activeTab === 'feedback' ? 'active' : ''} onClick={() => handleTabChange('feedback')}>Feedback & Support</li>
                </ul>
            </aside>
            <main className="settings-content">
                {activeTab === 'profile' && <ProfileSettings />}
                {activeTab === 'preference' && <PreferenceForm />}
                {activeTab === 'account' && <AccountSettings />}
                {activeTab === 'security' && <SecuritySettings />}
                {/* {activeTab === 'interaction' && <InteractionSettings />} */}
                {activeTab === 'content' && <ContentSettings />}
                {activeTab === 'accessibility' && <AccessibilitySettings />}
                {activeTab === 'location' && <LocationSettings />}
                {activeTab === 'community' && <CommunitySettings />}
                {activeTab === 'feedback' && <FeedbackSettings />}
            </main>
        </div>
    );
};

// Placeholder components for each section
const SecuritySettings = () => <div>Security Settings Content</div>;
const InteractionSettings = () => <div>Interaction Settings Content</div>;
const ContentSettings = () => <div>Content Settings Content</div>;
const AccessibilitySettings = () => <div>Accessibility Settings Content</div>;
const LocationSettings = () => <div>Location Settings Content</div>;
const CommunitySettings = () => <div>Community Settings Content</div>;
const FeedbackSettings = () => <div>Feedback Settings Content</div>;

export default SettingsPage;
