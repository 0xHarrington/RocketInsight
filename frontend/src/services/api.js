import axios from 'axios';

const API_BASE_URL = 'http://yourbackendapiurl.com'; // Replace with your actual backend API URL

export const fetchMarketData = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/all_markets`);
        return response.data;
    } catch (error) {
        console.error('Error fetching market data:', error);
        throw error;
    }
};