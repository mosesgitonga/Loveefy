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
import queue
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.INFO)

THRESHOLD_SCORE = 0

import uuid
import logging
class Recommender:
    def __init__(self, storage):
        self.storage = storage
        self.processed_pairs = set()

    def for_uninitialized_users(self, page, per_page):
        try:
            user_id = get_jwt_identity()
            user_profile = self.storage.get(User_profile, user_id=user_id)
            user_place = self.storage.get(Place, user_id=user_id)
            user_image = self.storage.get(Upload, user_id=user_id)

            desired_gender = 'female' if user_profile.gender == 'male' else 'male'
            desired_country = user_place.country

            profiles = self.storage.get_all(User_profile, use_and=True, gender=desired_gender, country=desired_country, page=page, per_page=per_page)
            user_ids = {profile.user_id for profile in profiles if profile.user_id != user_id}

            users = self.storage.get_multiple(User, ids=user_ids)
            places = self.storage.get_multiple(Place, ids=user_ids)
            images = self.storage.get_multiple(Upload, ids=user_ids)

            user_map = {user.id: user for user in users}
            place_map = {place.user_id: place for place in places}
            image_map = {image.user_id: image for image in images}

            recommendations = []

            for profile in profiles:
                user = user_map.get(profile.user_id)
                place = place_map.get(profile.user_id)
                image = image_map.get(profile.user_id)

                # Calculate the user's age from the DOB
                age = relativedelta(datetime.now(), profile.DOB).years

                recommendations.append({
                    "id": str(uuid.uuid4()),
                    "user_id1": user_id,
                    "user_id2": profile.user_id,
                    "opposite_id": user.id,
                    "score": 0, 
                    "first_name": profile.first_name,
                    "image_path": image.file_path if image else None,
                    "industry": profile.industry_major,
                    "country": place.country,
                    "region": place.region,
                    "age": age,
                    "gender": profile.gender
                })

            return recommendations

        except Exception as e:
            logging.error(f"Error: {e}")
            return {"message": "Internal Server Error"}, 500


    
    def recommend_users(self):
        """
        Utilizes both profile and preference information to recommend users.
        """
        try:
            users = self.storage.get_all(User) 

            logging.info(f"Total users: {len(users)}")

            # Fetch all preferences, profiles, and places in one go
            preferences = {pref.user_id: pref for pref in self.storage.get_all(Preference)}
            profiles = {profile.user_id: profile for profile in self.storage.get_all(User_profile)}
            places = {place.user_id: place for place in self.storage.get_all(Place)}

            recommendations = []  # Final list to store recommendations
            recommendations_queue = queue.Queue()  # Thread-safe queue
            users_length = len(users)

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(
                        self.process_user,
                        i,
                        users,
                        preferences,
                        profiles,
                        places,
                        recommendations_queue
                    )
                    for i in range(users_length)
                ]

                # Ensure all threads finish and log any exceptions
                for future in concurrent.futures.as_completed(futures):
                    if exception := future.exception():
                        logging.error(f"Thread encountered an error: {exception}")

            # Collect results from the queue into the recommendations list
            while not recommendations_queue.empty():
                recommendations.append(recommendations_queue.get())

            logging.info(f"Total recommendations to save: {len(recommendations)}")

            # Save recommendations to storage
            self.processed_pairs = set()
            for rec in recommendations:
                logging.info(f"user id 1: {rec['user_id1']}, user id 2: {rec['user_id2']}, score: {rec['score']}")
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

    def process_user(self, i, users, preferences, profiles, places, recommendations_queue):
        current_user = users[i]
        logging.info(f"Processing user: {current_user.id}")

        # Early return if any essential data is missing
        current_user_preference = preferences.get(current_user.id)
        current_user_profile = profiles.get(current_user.id)
        current_user_place = places.get(current_user.id)

        if not current_user or not current_user_preference or not current_user_profile or not current_user_place:
            logging.warning(f"Missing data for user {current_user.id}, skipping...")
            return

        # Process comparisons with other users
        for j in range(len(users)):
            if i == j:
                continue  

            other_user = users[j]

            # Skip already processed pairs
            pair = tuple(sorted((current_user.id, other_user.id)))
            if pair in self.processed_pairs:
                logging.info(f"Skipping already processed pair: {pair}")
                continue

            self.processed_pairs.add(pair)

            # Check if the recommendation already exists
            if self.storage.check_existing_recommendation(current_user.id, other_user.id):
                continue

            # Fetch data for the other user
            other_user_preference = preferences.get(other_user.id)
            other_user_profile = profiles.get(other_user.id)
            other_user_place = places.get(other_user.id)

            if not other_user or not other_user_preference or not other_user_profile or not other_user_place:
                logging.warning(f"Missing data for user {other_user.id}, skipping...")
                continue

            # Calculate the compatibility score
            score = self.calculate_score(
                current_user_place,
                other_user_place,
                current_user_preference,
                other_user_preference,
                current_user_profile,
                other_user_profile
            )

            if score == 0:
                logging.info(f"Pair {current_user.id}-{other_user.id} has no compatible score, skipping...")
                continue

            # Add to thread-safe queue
            recommendations_queue.put({
                "user_id1": current_user.id,
                "user_id2": other_user.id,
                "score": score
            })

            logging.info(f"Recommendation for pair {current_user.id}-{other_user.id} with score {score} added.")


    def calculate_score(self, current_user_place, other_user_place, current_user_preference, other_user_preference, current_user_profile, other_user_profile):
        try:
            logging.info(f"{current_user_preference.desired_gender}, {other_user_preference.desired_gender}")
            if self.is_gender_compatible(current_user_profile, current_user_preference, other_user_profile, other_user_preference) == False:
                logging.info("Gender not compatible")
                return 0

            score = self.calculate_basic_score()
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
        """
        # Check if other user's gender is in current user's preference
        if other_user_profile.gender in current_user_preference.desired_gender:
            if other_user_preference.desired_gender != current_user_profile.gender:
                return False
            return current_user_profile.gender in other_user_preference.desired_gender
        else:
            return False
    def is_age_compatible(self, current_user_profile, other_user_preference):
        return other_user_preference.min_age <= current_user_profile.age <= other_user_preference.max_age

    def calculate_basic_score(self):
        return 5

    def calculate_country_score(self, current_user_place, other_user_place):
        if current_user_place.country == other_user_place.country:
            return 25
        return 0
    
    def calculate_region_score(self, current_user_place, other_user_place):
        if current_user_place.region == other_user_place.region:
            return 11
        return 0
 
    def calculate_industry_score(self, current_user_profile, other_user_profile=None, other_user_preference=None):
        score = 0 

        if current_user_profile and other_user_preference: 
            if other_user_preference.desired_industry and current_user_profile.industry_major == other_user_preference.desired_industry:
                score += 16 
        return score

    # def calculate_hobby_score(self, current_user_preference, other_user_profile):
    #     return 4 if current_user_preference.fav_hobby == other_user_profile.fav_hobby else 0

    # def calculate_child_preference_score(self, current_user_preference, other_user_profile):
    #     return 7 if "any" in current_user_preference.wants_child and other_user_profile.has_child == "yes" else 0
    
    def fetch_recommendations(self, page=1, per_page=40):
        try:
            current_user_id = get_jwt_identity()
            current_user = self.storage.get(User, id=current_user_id)

            recommendations = self.storage.get_all(Recommendation, page=page, per_page=per_page, use_pagination=True, user_id1=current_user_id, user_id2=current_user_id)
            user_recommendations = [rec for rec in recommendations if rec.user_id1 == current_user_id or rec.user_id2 == current_user_id]

            if not user_recommendations:
                recommendations = self.for_uninitialized_users(page=page, per_page=per_page)
                return recommendations 

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


if __name__ == "__main__":
    storage = DbStorage()
    recommender = Recommender(storage)

    x = recommender.fetch_recommendations_from_profile("7b9a1bc7-72b2-43f2-8a5e-2d8343f246e5", page=1, per_page=10)
    print(x)