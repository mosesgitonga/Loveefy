from flask import jsonify, make_response
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

logging.basicConfig(level=logging.INFO)

THRESHOLD_SCORE = 5

class Recommender:
    def __init__(self):
        self.storage = DbStorage()

    def recommend_users(self):
        try:
            user_id = get_jwt_identity()
            current_user = self.storage.get(User, id=user_id)
            current_user_preference = self.storage.get(Preference, id=current_user.preference_id)
            current_user_profile = self.storage.get(User_profile, user_id=user_id)
            current_user_place = self.storage.get(Place, id=current_user.place_id)

            if not current_user or not current_user_preference or not current_user_profile:
                return make_response(jsonify([]), 200)  # Return an empty JSON array if any data is missing

            profiles = self.fetch_profiles()
            print('profiles', profiles)
            recommendations = []

            for other_profile in profiles:
                if other_profile.user_id == user_id:
                    continue  # Skip the current user 

                other_user = self.storage.get(User, id=other_profile.user_id)
                other_user_preference = self.storage.get(Preference, id=other_user.preference_id)
                other_user_place = self.storage.get(Place, id=other_user.place_id)
                print('place x',other_user_place.country)
                if not other_user_preference:
                    continue 

                score = self.calculate_score(current_user_place, other_user_place, current_user_preference, other_user_preference, current_user_profile, other_profile)
                print(f"Score for user {other_profile.user_id}: {score}")

                if score > THRESHOLD_SCORE:
                    recommendations.append({
                        "user_id": other_profile.user_id,
                        "score": score
                    })

            for rec in recommendations:
                new_recommendation = Recommendation(
                    id=str(uuid.uuid4()),
                    user_id1=user_id,
                    user_id2=rec['user_id'],
                    score=rec['score']
                )
                self.storage.new(new_recommendation)
            self.storage.save()

            return jsonify({"message": "Recommendations created successfully"}), 201
        except Exception as e:
            print(f"Error in recommend_users: {e}")
            return jsonify({'message': 'Internal Server Error'}), 500

    
    def fetch_profiles(self):
        return self.storage.get_all(User_profile)

    def calculate_score(self, current_user_place, other_user_place, current_user_preference, other_user_preference, current_user_profile, other_user_profile):
        try:
            score = 0

            if self.is_gender_compatible(current_user_preference, other_user_preference):
                logging.info("Gender not compatible")
                return 0

            if not self.is_age_compatible(current_user_profile, other_user_preference):
                logging.info("Age not compatible")
                return 0

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

            hobby_score = self.calculate_hobby_score(current_user_preference, other_user_profile)
            score += hobby_score if hobby_score is not None else 0
            logging.info(f"Score after hobby: {score}")

            child_preference_score = self.calculate_child_preference_score(current_user_preference, other_user_profile)
            score += child_preference_score if child_preference_score is not None else 0
            logging.info(f"Final score: {score}")

            return score
        except Exception as e:
            logging.error(f"Error in calculate_score: {e}")
            return 0

    def is_gender_compatible(self, current_user_preference, other_user_preference):
        return current_user_preference.gender == other_user_preference.gender

    def is_age_compatible(self, current_user_profile, other_user_preference):
        return other_user_preference.min_age <= current_user_profile.age <= other_user_preference.max_age

    def calculate_basic_score(self):
        return 5

    def calculate_country_score(self, current_user_place, other_user_place):
        if current_user_place.country == other_user_place.country:
            return 5
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
    
    def fetch_recommendations(self):
        """Fetches all recommendations associated with a certain user."""
        try:
            current_user_id = get_jwt_identity()
            recommendations = self.storage.get_all(Recommendation, user_id1=current_user_id)
            logging.info(recommendations)

            if recommendations:
                user_ids = [rec.user_id2 for rec in recommendations]
                users = self.storage.get_multiple(User, ids=user_ids)
                profiles = self.storage.get_multiple(User_profile, ids=user_ids)
                places = self.storage.get_multiple(Place, ids=[user.place_id for user in users])
                images = self.storage.get_multiple(Upload, ids=user_ids)

                user_map = {user.id: user for user in users}
                profile_map = {profile.user_id: profile for profile in profiles}
                place_map = {place.id: place for place in places}
                image_map = {image.user_id: image for image in images}

                recommendation_list = []
                for recommendation in recommendations:
                    other_user = user_map.get(recommendation.user_id2)
                    other_user_profile = profile_map.get(recommendation.user_id2)
                    other_user_place = place_map.get(other_user.place_id)
                    other_user_image = image_map.get(recommendation.user_id2)

                    recommendation_data = {
                        "id": recommendation.id,
                        "user_id1": recommendation.user_id1,
                        "user_id2": recommendation.user_id2,
                        "score": recommendation.score,
                        "username": other_user.username,
                        "image_path": other_user_image.image_path if other_user_image else None,
                        "industry": other_user_profile.industry_major if other_user_profile else None,
                        "country": other_user_place.country if other_user_place else None,
                        "region": other_user_place.region if other_user_place else None
                    }
                    recommendation_list.append(recommendation_data)

                return jsonify(recommendation_list), 200
            else:
                return jsonify([]), 200  

        except Exception as e:
            logging.error(f"Error fetching recommendations: {e}")
            return jsonify({"message": "Internal Server Error"}), 500     