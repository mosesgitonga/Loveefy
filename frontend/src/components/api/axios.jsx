import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000",
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to attach the token to every request
api.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('access_token');
    const excludedEndpoints = ['v1/auth/logins', 'v1/auth/registers'];

    if (!excludedEndpoints.includes(config.url) && token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response.status === 401) {
      // Handle unauthorized errors (e.g., redirect to login)
      console.error('Unauthorized access - redirecting to login');
      // Optionally, you could add logic to refresh the token here
    }
    return Promise.reject(error);
  }
);

export default api;
