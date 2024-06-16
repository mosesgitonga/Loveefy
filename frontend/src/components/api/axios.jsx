import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to attach the token to every request
//api.interceptors.request.use(
  //(config) => {
    // const token = localStorage.getItem('access_token') || sessionStorage.getItem('access_token');
    //const excludedEndpoints = ['api/auth/login', 'api/auth/register']; // Add other endpoints as needed

  //  if (!excludedEndpoints.includes(config.url) && token) {
  //    config.headers.Authorization = `Bearer ${token}`;
    //}
   // return config;
  //},
  //(error) => {
    //return Promise.reject(error);
  //}
//);

export default api;
