import axios from 'axios';

// Base URL for API requests - use environment variable or fallback to local development URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance with default config
const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

// Fetch the current state of the simulation
export const fetchSimulationState = async () => {
    try {
        const response = await apiClient.get('/simulation/state');
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Setup a new building for the simulation
export const setupBuilding = async (config) => {
    try {
        const response = await apiClient.post('/simulation/setup', config);
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Advance the simulation by one turn
export const advanceSimulation = async () => {
    try {
        const response = await apiClient.post('/simulation/advance');
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Add a zombie to a random room
export const addZombie = async () => {
    try {
        const response = await apiClient.post('/simulation/add-zombie');
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Add a practicante to a random room without zombies
export const addPracticante = async () => {
    try {
        const response = await apiClient.post('/simulation/add-practicante');
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Clean a room (remove zombies)
export const cleanRoom = async (floor, room) => {
    try {
        const response = await apiClient.post('/simulation/clean-room', { floor, room });
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Reset a sensor in a room
export const resetSensor = async (floor, room) => {
    try {
        const response = await apiClient.post('/simulation/reset-sensor', { floor, room });
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Toggle automatic zombie generation
export const toggleZombieGeneration = async () => {
    try {
        const response = await apiClient.post('/simulation/toggle-zombie-generation');
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Use the secret weapon to clean multiple rooms
export const triggerSecretWeapon = async () => {
    try {
        const response = await apiClient.post('/simulation/use-secret-weapon');
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Toggle automatic simulation running
export const autoRun = async (shouldRun) => {
    try {
        const response = await apiClient.post('/simulation/auto-run', { run: shouldRun });
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Reset the simulation
export const resetSimulation = async () => {
    try {
        const response = await apiClient.post('/simulation/reset');
        return response.data;
    } catch (error) {
        handleApiError(error);
        throw error;
    }
};

// Helper function to handle API errors
const handleApiError = (error) => {
    if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error('API Error Response:', error.response.data);
        console.error('Status:', error.response.status);
    } else if (error.request) {
        // The request was made but no response was received
        console.error('API Error Request:', error.request);
    } else {
        // Something happened in setting up the request that triggered an Error
        console.error('API Error Message:', error.message);
    }
}; 