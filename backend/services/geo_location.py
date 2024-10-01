from models.place import Place
from models.user import User
from models.engine.DBStorage import DbStorage
from models.user_profile import User_profile
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

storage = DbStorage()

class GeoLocation:
    def __init__(self):
        self.storage = storage 

    def geo_location(self, data):
        required_fields = ['latitude', 'longitude']
        for field in required_fields:
            if field not in data:
                return jsonify({"message": f"{field} is required"}), 400
        print('data: \n',data)
        try:
            user_id = get_jwt_identity()
            user = self.storage.get(User, id=user_id)
            if not user or not user.place_id:
                return jsonify({"message": "User not found or has no associated place"}), 404

            place = self.storage.get(Place, id=user.place_id)
            if not place:
                return jsonify({"message": "Place not found"}), 404

            # Update place coordinates
            place.latitude = data.get('latitude')
            place.longitude = data.get('longitude')

            self.storage.new(place)
            self.storage.save()
            print('location updated')
            return jsonify({"message": "Location updated successfully"}), 200  
        except Exception as e:
            print(e)
            return jsonify({"message": "Internal Server Error"}), 500  

    def get_location(self):
        try:
            # Gets the IDs of all users
            users = self.storage.get_all(User)
            user_profiles = self.storage.get_multiple(User_profile, ids=[user.id for user in users])
            places = self.storage.get_multiple(Place, ids=[user.place_id for user in users])

            # Create a map of place IDs to Place objects for quick access
            place_map = {place.id: place for place in places}

            user_locations = []

            for user in users:
                # Get user profile information
                profile = next((p for p in user_profiles if p.user_id == user.id), None)

                if profile and user.place_id:
                    # Get the associated place using the place_id from the user
                    place = place_map.get(user.place_id)
                    if place:
                        user_location = {
                            "id": user.id,
                            "name": user.username,
                            "longitude": place.longitude,
                            "latitude": place.latitude,
                            "email": user.email,
                        }
                        user_locations.append(user_location)

            # Return the user locations as a JSON response
            return jsonify(user_locations)

        except Exception as e:
            # Log the exception (consider using a logging framework)
            print("Error fetching user locations:", str(e))
            return jsonify({"message": "Internal Server Error"}), 500
