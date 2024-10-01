import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix the marker icons
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import api from '../api/axios';

// Set the default icon options for Leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerIcon2x,
  iconUrl: markerIcon,
  shadowUrl: markerShadow,
});

const UserMap = () => {
  const [userLocations, setUserLocations] = useState([]);

  useEffect(() => {
    const fetchUserLocations = async () => {
      try {
        const response = await api.get('/api/v1/admin/users/locations'); 
        // Access data directly from the response
        const validLocations = response.data.filter(user => user.latitude !== null && user.longitude !== null);
        setUserLocations(validLocations);
      } catch (error) {
        console.error('Error fetching user locations:', error);
      }
    };

    fetchUserLocations();
  }, []);

  // Set the center based on user locations if available
  const centerMap = userLocations.length > 0 ? 
    [userLocations[0].latitude, userLocations[0].longitude] : [0, 0];

  return (
    <MapContainer center={centerMap} zoom={2} style={{ height: '600px', width: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {userLocations.map((user) => (
        <Marker key={user.id} position={[user.latitude, user.longitude]}>
          <Popup>
            <div>
              <h3>{user.name}</h3>
              <p>Email: {user.email}</p>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default UserMap;
