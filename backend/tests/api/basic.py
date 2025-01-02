import requests
import random
from faker import Faker

faker = Faker()

BASE_URL = "http://localhost:5000"
HEADERS = {"Content-Type": "application/json"}
PASSWORD = "123456"

SCORE = 0
OVERALL_SCORE = 0


def generate_dummy_user():
    """Generate a random dummy user."""
    return f"user{random.randint(10, 999)}"


# Test Functions
def test_registration(base_url, headers, dummy_user, password):
    """Test user registration."""
    global SCORE, OVERALL_SCORE
    OVERALL_SCORE += 1
    payload = {"email": f"{dummy_user}@example.com", "password": password}
    url = f"{base_url}/v1/auth/registers"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Registration test is successful")
        SCORE += 1
    elif response.status_code == 409:
        print("User has already been registered")
        SCORE += 1
    else:
        print(f"Registration failed: {response.text} ({response.status_code})")
    return response


def test_login(base_url, headers, dummy_user, password):
    """Test user login."""
    global SCORE, OVERALL_SCORE
    OVERALL_SCORE += 1
    payload = {"email": f"{dummy_user}@example.com", "password": password}
    url = f"{base_url}/v1/auth/logins"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("Login test is successful")
        data = response.json()
        SCORE += 1
        return data.get('access_token')
    else:
        print(f"Login failed: {response.text} ({response.status_code})")
        return None


def test_create_profile(base_url, headers, dummy_user):
    """Test profile creation."""
    global SCORE, OVERALL_SCORE, gender
    OVERALL_SCORE += 1
    gender = random.choice(['male', 'female'])
    occupation = random.choice(['doctor', "teacher", "software engineer"])
    payload = {
        "gender": gender,
        "dob": "2001-12-10",
        "first_name": f"{dummy_user}",
        "occupation": occupation,
        "institution": faker.company(),
        "industry_major": faker.job(),
        "has_child": 0,
        "is_schooling": 1,
        "country": "ke",
        "region": "nyeri",
    }
    url = f"{base_url}/v1/profiles"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in (201, 200):
        print(f"Profile creation successful: {response.text}")
        SCORE += 1
    elif response.status_code == 409:
        print(f"Profile already exists: {response.text}")
        SCORE += 1
    else:
        print(f"Profile creation failed: {response.text} ({response.status_code})")
    return response


def test_create_preference(base_url, headers):
    """Test preference creation."""
    global SCORE, OVERALL_SCORE, gender

    OVERALL_SCORE += 1
    desired_gender = "female" if gender == "male" else "male"

    payload = {
        "desired_gender": desired_gender,
        "minAge": "18",
        "maxAge": "78",
        "desired_country": "ke",
        "desired_region": "nyeri",
        "desired_industry": "IT",
        "desired_education_level": "degree",
        "is_schooling": 0,
        "radius": 5,
    }

    url = f"{base_url}/v1/preferences"
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code in (201, 200):
        print(f"Preference creation successful: {response.text}")
        SCORE += 1
    elif response.status_code == 409:
        print(f"Preference already exists: {response.text}")
        SCORE += 1
    else:
        print(f"Preference creation failed: {response.text} ({response.status_code})")
    return response

def test_create_recommendation(base_url, headers):
    payload = {
        
    }


def run_tests():
    dummy_user = generate_dummy_user()

    test_registration(BASE_URL, HEADERS, dummy_user, PASSWORD)

    access_token = test_login(BASE_URL, HEADERS, dummy_user, PASSWORD)
    if access_token:
        HEADERS.update({"Authorization": f"Bearer {access_token}"})

        test_create_profile(BASE_URL, HEADERS, dummy_user)

        test_create_preference(BASE_URL, HEADERS)

    failed_tests = OVERALL_SCORE - SCORE
    print(f"\nSummary: {SCORE}/{OVERALL_SCORE} tests passed, {failed_tests} failed.")

if __name__ == "__main__":
    run_tests()
