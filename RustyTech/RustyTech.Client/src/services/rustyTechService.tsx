import axios from 'axios';

const API_URL = 'https://localhost:5001/api';


//maybe name this function getRegisterData
export const fetchData = async () => {
    try {
        const response = await axios.get(`${API_URL}/register`);
        return response.data;

    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }

};