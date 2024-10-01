import api from "../api/axios";

const fetchLocation = () => {
    if (navigator.geolocation) {
        const options = {
            enableHighAccuracy: true, 
            timeout: 10000, 
            maximumAge: 0 
        };

        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
                
                // Send location to backend
                api.post('/api/v1/geo_location', { latitude, longitude })
                    .then(response => console.log('Location sent:', response))
                    .catch(error => {
                        console.error('Error sending location:', error);
                        alert('Failed to send location to the server.');
                    });
            },
            (error) => {
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        alert('Location permission denied by the user.');
                        break;
                    case error.POSITION_UNAVAILABLE:
                        alert('Location information is unavailable.');
                        break;
                    case error.TIMEOUT:
                        alert('Request to get location timed out.');
                        break;
                    default:
                        alert('An unknown error occurred while fetching location.');
                        break;
                }
                console.error('Error getting location:', error.message);
            },
            options
        );
    } else {
        alert('Geolocation is not supported by this browser.');
    }
};

export default fetchLocation;

