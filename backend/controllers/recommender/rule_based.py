from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity
from models.engine.DBStorage import DbStorage
from models.user import User
from models.recommendation import Recommendation
from models.user_profile import User_profile
from models.preference import Preference
from models.place import Place
from models.uploads import Upload
import uuid
import logging
from datetime import datetime
import concurrent.futures

logging.basicConfig(level=logging.INFO)

THRESHOLD_SCORE = 0

class Recommender:
    def __init__(self):
        self.storage = DbStorage()
        self.processed_pairs = set()  

    def recommend_users(self):
        try:
            users = self.storage.get_all(User) 

            logging.info(f"Total users: {len(users)}")

            # Fetch all preferences, profiles, and places in one go
            preferences = {pref.id: pref for pref in self.storage.get_all(Preference)}
            profiles = {profile.user_id: profile for profile in self.storage.get_all(User_profile)}
            places = {place.id: place for place in self.storage.get_all(Place)}

            recommendations = []
            users_length = len(users)
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for i in range(users_length):
                    futures.append(executor.submit(self.process_user, i, users, preferences, profiles, places, recommendations))
                
                concurrent.futures.wait(futures)

            logging.info(f"Total recommendations to save: {len(recommendations)}")
            self.processed_pairs = set()
            for rec in recommendations:
                new_recommendation = Recommendation(
                    id=str(uuid.uuid4()),
                    user_id1=rec['user_id1'],
                    user_id2=rec['user_id2'],
                    score=rec['score']
                )
                self.storage.new(new_recommendation)
            self.storage.save()

            return {"message": "Recommendations created successfully"}, 201
        except Exception as e:
            logging.error(f"Error in recommend_users: {e}")
            return {'message': 'Internal Server Error'}

    def process_user(self, i, users, preferences, profiles, places, recommendations):
        current_user = users[i]
        logging.info(f"Current user: {current_user.id}")

        current_user_preference = preferences.get(current_user.preference_id)
        current_user_profile = profiles.get(current_user.id)
        current_user_place = places.get(current_user.place_id)

        if not current_user or not current_user_preference or not current_user_profile or not current_user_place:
            logging.warning(f"Missing data for current user {current_user.id}")
            return

        for j in range(len(users)):
            if i == j:
                continue  # Skip comparing user to themselves

            other_user = users[j]

            pair = tuple(sorted((current_user.id, other_user.id)))

            if pair in self.processed_pairs:
                logging.info(f"Skipping already processed pair: {pair}")
                continue  

            self.processed_pairs.add(pair)

            # ensuring no duplicate recommendation.
            if self.storage.check_existing_recommendation(current_user.id, other_user.id):
                continue

            other_user_preference = preferences.get(other_user.preference_id)
            other_user_profile = profiles.get(other_user.id)
            other_user_place = places.get(other_user.place_id)

            if not other_user or not other_user_preference or not other_user_profile or not other_user_place:
                logging.warning(f"Missing data for other user {other_user.id}")
                continue  
            
            score = self.calculate_score(current_user_place, other_user_place, current_user_preference, other_user_preference, current_user_profile, other_user_profile)
            logging.info(f"Calculated score for pair {current_user.id}-{other_user.id}: {score}")

            if score > THRESHOLD_SCORE:
                recommendations.append({
                    "user_id1": current_user.id,
                    "user_id2": other_user.id,
                    "score": score 
                })

    def calculate_score(self, current_user_place, other_user_place, current_user_preference, other_user_preference, current_user_profile, other_user_profile):
        try:
            score = 0
            if self.is_gender_compatible(current_user_profile, current_user_preference, other_user_profile, other_user_preference) == False:
                logging.info("Gender not compatible")
                score = 0
                return score

            score += self.calculate_basic_score()
            logging.info(f"Basic score: {score}")

            if other_user_place:
                country_score = self.calculate_country_score(current_user_place, other_user_place)
                score += country_score if country_score is not None else 0
                logging.info(f"Score after country: {score}")
            else:
                logging.warning("Other user place is None")

            industry_score = self.calculate_industry_score(current_user_profile, other_user_preference)
            score += industry_score if industry_score is not None else 0
            logging.info(f"Score after industry: {score}")

            return score
        except Exception as e:
            logging.error(f"Error in calculate_score: {e}")
            return 0

    def is_gender_compatible(self, current_user_profile, current_user_preference, other_user_profile, other_user_preference):
        """
        Checks compatibility based on gender preferences.

        This function assumes a user's preference can include multiple genders.
        Compatibility is considered true if:
        - The current user's preference includes the other user's gender.
        - The other user's preference includes the current user's gender.

        Args:
            current_user_profile (object): Current user's profile information.
            current_user_preference (object): Current user's gender preference.
            other_user_profile (object): Other user's profile information.
            other_user_preference (object): Other user's gender preference.

        Returns:
            bool: True if compatible, False otherwise.
        """

        # Check if other user's gender is in current user's preference
        if other_user_profile.gender in current_user_preference.gender:
            if other_user_preference.gender != current_user_profile.gender:
                return False
            # Check if current user's gender is in other user's preference (ensures mutual interest)
            return current_user_profile.gender in other_user_preference.gender
        else:
            return False
    def is_age_compatible(self, current_user_profile, other_user_preference):
        return other_user_preference.min_age <= current_user_profile.age <= other_user_preference.max_age

    def calculate_basic_score(self):
        return 5

    def calculate_country_score(self, current_user_place, other_user_place):
        if current_user_place.country == other_user_place.country:
            return 10
        return 0
    
    def calculate_region_score(self, current_user_place, other_user_place):
        if current_user_place.region == other_user_place.region:
            return 11
        return 0
 
    def calculate_industry_score(self, current_user_profile, other_user_preference):
        score = 0
        if current_user_profile.industry_major == other_user_preference.industry_major:
            score += 12
        return score

    def calculate_hobby_score(self, current_user_preference, other_user_profile):
        return 4 if current_user_preference.fav_hobby == other_user_profile.fav_hobby else 0

    def calculate_child_preference_score(self, current_user_preference, other_user_profile):
        return 7 if "any" in current_user_preference.wants_child and other_user_profile.has_child == "yes" else 0
    
    def fetch_recommendations(self, page=1, per_page=12):
        try:
            current_user_id = get_jwt_identity()
            current_user = self.storage.get(User, id=current_user_id)

            recommendations = self.storage.get_all(Recommendation, page=page, per_page=per_page, user_id1=current_user_id, user_id2=current_user_id)
            user_recommendations = [rec for rec in recommendations if rec.user_id1 == current_user_id or rec.user_id2 == current_user_id]

            if not user_recommendations:
                logging.info("No recommendations found")
                return [{"recommendations": []}], 200

            user_ids = set()
            for rec in user_recommendations:
                other_user_id = rec.user_id2 if rec.user_id1 == current_user_id else rec.user_id1
                user_ids.add(other_user_id)

            users = self.storage.get_multiple(User, ids=list(user_ids))
            profiles = self.storage.get_multiple(User_profile, ids=user_ids)
            places = self.storage.get_multiple(Place, ids=[user.place_id for user in users])
            images = self.storage.get_multiple(Upload, ids=user_ids)

            user_map = {user.id: user for user in users if user}
            profile_map = {profile.user_id: profile for profile in profiles if profile}
            place_map = {place.id: place for place in places if place}
            image_map = {image.user_id: image for image in images if image}

            current_user_preference = self.storage.get(Preference, id=current_user.preference_id)
            if not current_user_preference:
                return {"message": "Internal Server Error"}, 500

            recommendation_list = []

            for recommendation in user_recommendations:
                other_user_id = recommendation.user_id2 if recommendation.user_id1 == current_user_id else recommendation.user_id1
                other_user = user_map.get(other_user_id)
                other_user_profile = profile_map.get(other_user_id)
                other_user_place = place_map.get(other_user.place_id if other_user else None)
                other_user_image = image_map.get(other_user_id)

                if recommendation.score < 5:
                    continue

                age = None
                if other_user_profile and other_user_profile.DOB:
                    dob = other_user_profile.DOB
                    if isinstance(dob, datetime):
                        dob = dob.strftime('%Y-%m-%d') 
                    today = datetime.today()
                    dob_datetime = datetime.strptime(dob, '%Y-%m-%d')  
                    age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))                
                else:
                    age = None

                opposite_id = recommendation.user_id2 if recommendation.user_id1 == current_user_id else recommendation.user_id1

                recommendation_data = {
                    "id": recommendation.id,
                    "user_id1": recommendation.user_id1,
                    "user_id2": recommendation.user_id2,
                    "opposite_id": opposite_id,
                    "score": recommendation.score,
                    "username": other_user.username.upper(),
                    "image_path": other_user_image.image_path if other_user_image else None,
                    "industry": other_user_profile.industry_major.upper() if other_user_profile else None,
                    "country": other_user_place.country if other_user_place else None,
                    "region": other_user_place.region if other_user_place else None,
                    "age": age,
                    "gender": other_user_profile.gender if other_user_profile else None
                }

                recommendation_list.append(recommendation_data)

            return recommendation_list, 200
            
        except Exception as e:
            logging.error(f"Error fetching recommendations: {e}")
            return {"error": "Internal Server Error"}, 500
