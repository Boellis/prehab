/*
Main App component that manages view switching between login, register, dashboard, and collection.
*/
import React, { useState } from 'react';
import { LoginForm } from './components/LoginForm';
import { RegisterForm } from './components/RegisterForm';
import { ExerciseDashboard } from './components/ExerciseDashboard';
import { CollectionDashboard } from './components/CollectionDashboard';
import { AdminDashboard } from './components/AdminDashboard';
import API from './api/axios';
import logo from './assets/logo.png';

const App: React.FC = () => {
  // Token and view state.
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));
  const [view, setView] = useState<'login' | 'register' | 'dashboard' | 'collection' | 'admin'>(token ? 'dashboard' : 'login');
  const [useCloudData, setUseCloudData] = useState(false);

  // Handlers for login, logout, refresh.
  const handleLogin = (jwt: string, refreshToken: string) => {
    localStorage.setItem('token', jwt);
    localStorage.setItem('refresh_token', refreshToken);
    setToken(jwt);
    setView('dashboard');
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh_token');
    setToken(null);
    setView('login');
  };

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

  // Decide whether to show the logo.
  const showLogo = view === 'login' || view === 'register';

  return (
    <div style={{ display: 'flex', padding: '20rem' ,  transformOrigin: 'center left', paddingTop: '10rem'}}>
      {/* Left side: content */}
      <div style={{ flex: '1', textAlign: 'center' }}>
        <h1>[P]rehab Takehome</h1>
        {token && (
          <div style={{ marginBottom: '1rem' }}>
            {/* Use a separate NavBar component or inline buttons with consistent style */}
            <button onClick={handleLogout} style={{ padding: '0.75rem 1rem' }}>Logout</button>
            <button onClick={handleRefreshToken} style={{ padding: '0.75rem 1rem', marginLeft: '1rem' }}>Refresh Token</button>
            <button onClick={() => setView('dashboard')} style={{ padding: '0.75rem 1rem', marginLeft: '1rem' }}>Dashboard</button>
            <button onClick={() => setView('collection')} style={{ padding: '0.75rem 1rem', marginLeft: '1rem' }}>My Collection</button>
            <button onClick={() => setView('admin')} style={{ padding: '0.75rem 1rem', marginLeft: '1rem' }}>Admin Dashboard</button>
          </div>
        )}

        {/* Render the main view */}
        {view === 'login' && <LoginForm onSuccess={handleLogin} onSwitch={() => setView('register')} />}
        {view === 'register' && <RegisterForm onSuccess={() => setView('login')} onSwitch={() => setView('login')} />}
        {view === 'dashboard' && token && <ExerciseDashboard token={token} useCloudData={useCloudData} />}
        {view === 'collection' && token && <CollectionDashboard />}
        {view === 'admin' && token && <AdminDashboard useCloudData={useCloudData} setUseCloudData={setUseCloudData} />}
      </div>

      {/* Right side: logo only on login/register */}
      {showLogo && (
        <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end', alignItems: 'flex-start', //transform: 'scale(1.25)',
          padding: '100px' }}>
          <img src={logo} alt="Prehab Takehome Logo" style={{ width: '300px', margin: '1rem' }} />
        </div>
      )}
    </div>
  );
};

export default App;