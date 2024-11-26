import requests
import json

# API Endpoints
BASE_URL = "https://www.loveefy.africa/api/v1"
LOGIN_URL = f"{BASE_URL}/auth/logins"
PROFILES_URL = f"{BASE_URL}/profiles"

# File paths
DUMMY_USERS_FILE = "dummy_users.json"
DUMMY_PROFILES_FILE = "/home/moses/Downloads/dummy_profiles.json"

# Common credentials
PASSWORD = "123"
EMAIL_DOMAIN = "@example.com"

def load_users(file_path):
    """Load dummy users from the JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def load_profiles(file_path):
    """Load dummy profiles from the JSON file."""
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

def create_profile(profile, token):
    """Create a profile using the provided access token."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(PROFILES_URL, json=profile, headers=headers)
    if response.status_code == 201:
        print(f"Profile created for {profile['username']}")
    else:
        print(f"Failed to create profile for {profile['username']}: {response.text}")

def main():
    """Main function to process users and profiles."""
    users = load_users(DUMMY_USERS_FILE)
    profiles = load_profiles(DUMMY_PROFILES_FILE)
    
    # Map usernames to profiles
    profile_map = {profile["username"]: profile for profile in profiles}
    
    for user in users:
        username = user["username"]
        email = f"{username}{EMAIL_DOMAIN}"
        token = login(email, PASSWORD)
        if token:
            profile = profile_map.get(username)
            if profile:
                create_profile(profile, token)
            else:
                print(f"No profile found for username: {username}")

if __name__ == "__main__":
    main()
