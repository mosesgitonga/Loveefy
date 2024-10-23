import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Signup from './components/auth/signup';
import Login from './components/auth/login';
import Profile from './components/profile/profile';
import PreferenceForm from './components/preferences/preferences';
import Upload from './components/uploads/Upload_pic';
import Discovery from './components/discovery/discoveryPage';
import InitiatedChats from './components/messages/initiatedChats';
import ChatBox from './components/messages/chatBox';
import Notifications from './components/notifications/notification';
import SettingsPage from './components/settings/settingsPage';
import ForgotPassword from './components/verifications/forgotPassword';
import Upgrade from './components/upgrade/upgrade';
import UserProfile from './components/profile/currentUserProfile';
import FeedbackForm from './components/feedback';
import SuperAdminPage from './components/admin/superAdmin';
import Gallery from './components/profile/galleryPage';
import BlogDetails from './pages/Blog/BlogDetails';
import ScrollToTop from './components/common/ScrollToTop';
import Landing from './pages/landing/Landing';

export default function App() {
  return (
    <Router>
      <ScrollToTop />
      <Routes>
        <Route path='/' element={<Landing />} />
        <Route path='/articles/:slug' element={<BlogDetails />} />
        <Route path='/register' element={<Signup />} />
        <Route path='/login' element={<Login />} />
        <Route path='/profile/setup' element={<Profile />} />
        <Route path='/preference' element={<PreferenceForm />} />
        <Route path='/upload' element={<Upload />} />
        <Route path='/discovery/home' element={<Discovery />} />
        <Route path='/discovery/chats' element={<InitiatedChats />} />
        <Route path='/discovery/notifications' element={<Notifications />} />
        <Route path='/c/:roomId' element={<ChatBox />} />
        <Route path='/discovery/settings' element={<SettingsPage />} />
        <Route path='/auth/otp-request' element={<ForgotPassword />} />
        <Route path='/hello_user' element={<Upgrade />} />
        <Route path='/profile/:userId' element={<UserProfile />} />
        <Route path='/feedback' element={<FeedbackForm />} />
        <Route path='/gallery' element={<Gallery />} />
        <Route path='/super/admin/moses' element={<SuperAdminPage />} />
      </Routes>
    </Router>
  );
}
