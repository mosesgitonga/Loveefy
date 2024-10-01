import axios from 'axios';

const api = axios.create({
  baseURL: "https://www.loveefy.africa",
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to attach the token to every request
api.interceptors.request.use(
  (config) => {
    const token = sessionStorage.getItem('access_token');
    console.log('token', token)
    const excludedEndpoints = ['api/v1/auth/logins', 'api/v1/auth/registers'];

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
      NavigationPreloadManager

    }
    console.log(error)
    return Promise.reject(error);
  }
);


export default api;
