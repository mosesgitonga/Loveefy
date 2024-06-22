import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import IndexPage from './components'
import Signup from './components/auth/signup';
import Login from './components/auth/login';
import Profile from './components/profile/profile';
import PreferenceForm from './components/preferences/preferences';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path='/' element={<IndexPage />} />
        <Route path='/register' element={<Signup />} />
        <Route path='/login' element={<Login />}/>
        <Route path='/profile/setup' element={<Profile />} />
        <Route path='/preference' element={<PreferenceForm />} />
      </Routes>
    </Router>
  </React.StrictMode>,
)
