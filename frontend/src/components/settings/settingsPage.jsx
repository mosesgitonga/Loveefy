import React, { useState } from 'react';
import './settingsPage.css'; 
import ProfileSettings from './profile';
import PreferenceForm from './preferences/preference';
import AccountSettings from './account/account'

const SettingsPage = () => {
    const [activeTab, setActiveTab] = useState('profile');

    const handleTabChange = (tab) => {
        setActiveTab(tab);
    };

    return (
        <div className="settings-page">
            <aside className="settings-sidebar">
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
                {activeTab == 'preference' && <PreferenceForm />}
                {activeTab === 'account' && <AccountSettings />}
                {activeTab === 'security' && <SecuritySettings />}
                {activeTab === 'interaction' && <InteractionSettings />}
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
