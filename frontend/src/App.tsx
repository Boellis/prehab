/*
Main App component that manages view switching between login, register, dashboard, and collection.
*/

import React, { useState } from 'react';
import { LoginForm } from './components/LoginForm';
import { RegisterForm } from './components/RegisterForm';
import { ExerciseDashboard } from './components/ExerciseDashboard';
import { CollectionDashboard } from './components/CollectionDashboard';
import API from './api/axios';
import logo from './assets/logo.png';

const App: React.FC = () => {
  // State to store the JWT token.
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
  // State to manage the current view: login, register, dashboard, or collection.
  const [view, setView] = useState<'login' | 'register' | 'dashboard' | 'collection'>(token ? 'dashboard' : 'login');

  // Handle successful login by saving tokens and switching to the dashboard.
  const handleLogin = (jwt: string, refreshToken: string) => {
    localStorage.setItem('token', jwt);
    localStorage.setItem('refresh_token', refreshToken);
    setToken(jwt);
    setView('dashboard');
  };

  // Logout by clearing tokens and switching back to login view.
  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setView('login');
  };

  // Handle token refresh via the backend.
  const handleRefreshToken = async () => {
    const storedRefreshToken = localStorage.getItem('refresh_token');
    if (!storedRefreshToken) {
      alert("No refresh token found. Please log in again.");
      handleLogout();
      return;
    }

    try {
      const res = await API.post('/auth/refresh', { refresh_token: storedRefreshToken });
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('refresh_token', res.data.refresh_token);
      setToken(res.data.access_token);
      alert('Token refreshed successfully!');
    } catch {
      alert('Token refresh failed. Please log in again.');
      handleLogout();
    }
  };



  return (
    <div style={{ display: 'flex', padding: '1rem' ,  transform: 'scale(1.75)', transformOrigin: 'top left'}}>
      {/* Left side: all text and forms aligned to left */}
      <div style={{ flex: '1', textAlign: 'left' }}>
        <h1>Prehab Takehome</h1>
        {token && (
          <div style={{ marginBottom: '1rem' }}>
            <button onClick={handleLogout}>Logout</button>
            <button onClick={handleRefreshToken} style={{ marginLeft: '1rem' }}>Refresh Token</button>
            <button onClick={() => setView('dashboard')} style={{ marginLeft: '1rem' }}>Dashboard</button>
            <button onClick={() => setView('collection')} style={{ marginLeft: '1rem' }}>My Collection</button>
          </div>
        )}

        {view === 'login' && <LoginForm onSuccess={handleLogin} onSwitch={() => setView('register')} />}
        {view === 'register' && <RegisterForm onSuccess={() => setView('login')} onSwitch={() => setView('login')} />}
        {view === 'dashboard' && token && <ExerciseDashboard token={token} />}
        {view === 'collection' && token && <CollectionDashboard />}
      </div>

      {/* Right side: Logo on the right half */}
      <div style={{ flex: '1', display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-start' }}>
        <img 
          src={logo} 
          alt="Prehab Takehome Logo" 
          style={{ width: '300px', margin: '5rem' , marginTop: '0px'}}
        />
      </div>
    </div>
  );
};

export default App;
