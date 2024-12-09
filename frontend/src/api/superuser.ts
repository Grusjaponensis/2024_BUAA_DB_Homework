import server from './server';
import snackbar from '../api/snackbar'

export const getUsers = async() => {
    try {
        const response = await server.get(
            '/users/?skip=0&limit=100',
            { "Content-Type" : "application/json" }
        );
        if (response != null && response.status === 200 ) {
            return response.data;
        } else {
            snackbar.error("Error getting users");
            console.log("Error getting users: " + response)
        }
    } catch (error) {
        console.log("Error getting users: " + error)
    }
}