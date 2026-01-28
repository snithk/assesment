import axios from 'axios';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

// Use localhost for Android emulator (10.0.2.2) or local IP for device
// For Windows development with Android emulator:
const API_URL = 'http://172.31.161.88:5000';
// If generic fetch fails, we might need the actual IP of the machine.
// Assuming Android Emulator for now.

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor to add token
api.interceptors.request.use(async (config) => {
    const token = await SecureStore.getItemAsync('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            await SecureStore.deleteItemAsync('token');
            // Ideally redirect to login, but we are in a service. 
            // The UI will likely handle the null token state eventually or user restarts.
        }
        return Promise.reject(error);
    }
);

export const authService = {
    signup: async (name, email, password) => {
        const response = await api.post('/auth/signup', { name, email, password });
        if (response.data.token) {
            await SecureStore.setItemAsync('token', response.data.token);
        }
        return response.data;
    },
    login: async (email, password) => {
        const response = await api.post('/auth/login', { email, password });
        if (response.data.token) {
            await SecureStore.setItemAsync('token', response.data.token);
        }
        return response.data;
    },
    logout: async () => {
        try {
            await api.post('/auth/logout');
        } catch (e) {
            // ignore
        }
        await SecureStore.deleteItemAsync('token');
    },
    me: async () => {
        const response = await api.get('/auth/me');
        return response.data;
    }
};

export const videoService = {
    getDashboard: async () => {
        const response = await api.get('/dashboard');
        return response.data;
    },
    getStreamUrl: async (videoId, token) => {
        // Pass token as query param as per requirement
        const response = await api.get(`/video/${videoId}/stream?token=${token}`);
        return response.data;
    }
};

export default api;
