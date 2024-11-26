import requests
import json

# API Endpoints
BASE_URL = "https://www.loveefy.africa/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/logins"
PREFERENCES_URL = f"{BASE_URL}/preferences"  # Corrected the route

# File paths
DUMMY_USERS_FILE = "dummy_users.json"
DUMMY_PREFERENCES_FILE = "/home/moses/Downloads/dummy_preferences_opposite_gender.json"

# Common credentials
PASSWORD = "123"
EMAIL_DOMAIN = "@example.com"

def load_users(file_path):
    """Load dummy users from the JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def load_preferences(file_path):
    """Load dummy preferences from the JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def login(email, password):
    """Log in to get the access token for a user."""
    response = requests.post(LOGIN_URL, json={"email": email, "password": password})
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"Login failed for {email}: {response.text}")
        return None

def create_preference(preference, token):
    """Create a preference using the provided access token."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(PREFERENCES_URL, json=preference, headers=headers)
    if response.status_code == 201:
        print(f"Preference created for {preference['username']}")
    else:
        print(f"Failed to create preference for {preference['username']}: {response.text}")

def main():
    """Main function to process users and preferences."""
    users = load_users(DUMMY_USERS_FILE)
    preferences = load_preferences(DUMMY_PREFERENCES_FILE)
    
    # Map usernames to preferences
    preference_map = {preference["username"]: preference for preference in preferences}
    
    for user in users:
        username = user["username"]
        email = f"{username}{EMAIL_DOMAIN}"
        token = login(email, PASSWORD)
        if token:
            preference = preference_map.get(username)
            if preference:
                create_preference(preference, token)
            else:
                print(f"No preference found for username: {username}")

if __name__ == "__main__":
    main()
