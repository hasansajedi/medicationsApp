import axios from 'axios';

async function getAccessToken() {
    try {
        const credential = "grant_type=password&username=password&password=password&client_secret=" + process.env.REACT_APP_SHRED_ACCESS_KEY;
        const url = process.env.REACT_APP_BACKEND_URL + 'api/auth/token';

        const response = await axios.post(url, credential, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        });
        if (response.status === 201 && response.data.access_token) {
            return response.data.access_token;
        } else {
            throw new Error('Authentication failed');
        }
    } catch (error) {
        console.error('Error while retrieving access token:', error);
        throw error;
    }
}

export default getAccessToken;
