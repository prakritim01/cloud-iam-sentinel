import axios from 'axios';

const API_URL = "http://localhost:8000"; // Ensure this matches your backend port

export const scanPolicy = async (policyText) => {
    try {
        const response = await axios.post(`${API_URL}/scan`, {
            policy: policyText
        });
        return response.data;
    } catch (error) {
        console.error("Scanning Error:", error);
        throw error;
    }
};