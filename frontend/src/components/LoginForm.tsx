/* 
A login form component for user authentication.
*/

import React, { useState } from 'react';
import API from '../api/axios';

interface LoginFormProps {
  onSuccess: (jwt: string, refreshToken: string) => void;
  onSwitch: () => void;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSuccess, onSwitch }) => {
  // Local state for username and password.
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Function to perform login.
  const login = async () => {
    try {
      // Send POST request to backend auth/login endpoint.
      const res = await API.post('/auth/login', { username, password });
      // On success, invoke onSuccess callback with tokens.
      onSuccess(res.data.access_token, res.data.refresh_token);
      localStorage.setItem('user_id', String(res.data.user_id));
    } catch {
      alert('Login failed. Please check your credentials.');
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',      // Center horizontally
      gap: '0.5rem',             // Space between items
      transform: 'scale(1.5)',
      padding: '100px'
    }}>
      <h2>Login</h2>
      <input
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
        style={{ padding: '0.5rem', width: '200px' }}
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
        style={{ padding: '0.5rem', width: '200px' }}
      />
      <button onClick={login} style={{ padding: '0.5rem 1rem' }}>
        Login
      </button>
      <p>
        Don't have an account? <button onClick={onSwitch}>Register</button>
      </p>
    </div>
  );
};