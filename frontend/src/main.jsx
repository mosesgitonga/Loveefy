import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import IndexPage from './components'
import Signup from './components/auth/signup';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <Routes>
        <Route path='/' element={<IndexPage />} />
        <Route path='/register' element={<Signup />} />
      </Routes>
    </Router>
  </React.StrictMode>,
)
