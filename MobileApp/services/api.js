import axios from 'axios';

// Replace this with your actual Render URL (e.g., https://your-backend.onrender.com)
// Your exact Wi-Fi IP automatically retrieved for the physical phone to connect:
const RENDER_URL = 'https://binary-image-qnn-new.onrender.com';
const NGROK_URL = 'https://founder-dangling-sacred.ngrok-free.dev'; 

const BASE_URL = NGROK_URL; // Connecting via ngrok for remote access

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true',
  },
});

export const predictDigit = async (base64Image, actualDigit) => {
  try {
    const response = await api.post('/MnistTorchQNN/', {
      image: `data:image/png;base64,${base64Image}`,
      actual: actualDigit,
    });
    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

export default api;
