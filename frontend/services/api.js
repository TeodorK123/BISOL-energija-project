import axios from 'axios';

const API_URL = 'http://localhost:8000';

export const getCustomerData = async (customerId) => {
    try {
        const response = await axios.get(`${API_URL}/customers/${customerId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching customer data:", error);
        return null;
    }
};