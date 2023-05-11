import React from 'react';
import './App.css';

import { Routes, Route, BrowserRouter } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Settings from './pages/Settings';
import Profile from './pages/Profile';
import Issues from './pages/Issues';
import Home from './pages/Home';


const App = () => {
  return (
    <div className="App">
      <BrowserRouter>
      <Routes>
        <Route index element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />}>
          <Route path="settings" element={<Settings />} />
          <Route path="profile" element={<Profile />} />
          <Route path="issues" element={<Issues />} />
        </Route>
      </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
