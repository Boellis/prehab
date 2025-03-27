/**
This file sets up an Axios instance for API calls to the backend.
It automatically includes the JWT token from localStorage in every request.
**/

import axios from 'axios';

// Create an Axios instance with the backend URL.
const API = axios.create({
  baseURL: 'http://localhost:8000', // Backend URL; adjust if necessary.
});

// Add a request interceptor to include the JWT token from localStorage.
API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    // Ensure headers object exists.
    config.headers = config.headers || {};
    // Set the Authorization header with the Bearer token.
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default API;
