import axios from 'axios';

export async function searchDrugs(searchQuery, page = 1) {
    const accessToken = localStorage.getItem('access_token');
    try {
        if (!process.env.REACT_APP_BACKEND_URL) {
            console.error("The REACT_APP_BACKEND_URL environment variable is not defined.");
            throw new Error("The REACT_APP_BACKEND_URL environment variable is not defined.");
        }
        if (!process.env.REACT_APP_SHRED_ACCESS_KEY) {
            console.error("The REACT_APP_SHRED_ACCESS_KEY environment variable is not defined.");
            throw new Error("The REACT_APP_SHRED_ACCESS_KEY environment variable is not defined.");
        }

        const API_BASE_URL = process.env.REACT_APP_BACKEND_URL + 'api/drugs/';
        let apiUrl = `${API_BASE_URL}?page=${page}`;
        if (searchQuery) {
            apiUrl += `&search=${searchQuery}`;
        }
        const response = await axios.get(apiUrl, {
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        });
        return response.data;
    } catch (error) {
        throw error;
    }
}