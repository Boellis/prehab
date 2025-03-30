/*
A registration form component for creating new users.
*/

import React, { useState } from 'react';
import API from '../api/axios';

interface RegisterFormProps {
  onSuccess: () => void;
  onSwitch: () => void;
}

export const RegisterForm: React.FC<RegisterFormProps> = ({ onSuccess, onSwitch }) => {
  // Local state for registration fields.
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  // Function to perform registration.
  const register = async () => {
    try {
      // Send POST request to backend auth/register endpoint.
      await API.post('/auth/register', { username, password });
      onSuccess();
    } catch (err) {
      alert('Registration failed. Make sure the backend is running and username is unique.');
      console.error(err);
    }
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',      // Center horizontally
      justifyContent: 'center',  // Center vertically if parent has enough height
      gap: '0.5rem',             // Space between items
      transform: 'scale(1.5)',
      padding: '100px'              // Space between items
    }}>
      <h2>Register</h2>
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
      <button onClick={register} style={{ padding: '0.5rem 1rem' }}>
        Register
      </button>
      <p>
        Already have an account? <button onClick={onSwitch}>Login</button>
      </p>
    </div>
  );
};