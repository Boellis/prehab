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
    <div>
      <h2>Register</h2>
      <input value={username} onChange={e => setUsername(e.target.value)} placeholder="Username" />
      <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="Password" />
      <button onClick={register}>Register</button>
      <p>
        Already have an account? <button onClick={onSwitch}>Login</button>
      </p>
    </div>
  );
};
