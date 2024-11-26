import requests
import json 

json_file = "./dummy_users.json"
with open(json_file, 'r') as file:
    users = json.load(file)

api_url = "https://www.loveefy.africa/api/v1/auth/registers"

for user in users:
    try:
        response = requests.post(api_url, json=user)
        if response.status_code == 201:
            print('user registered successfully')
        else:
            print(f"failed to register user {response.status_code}")
        
    except Exception as e:
        print("an error occured: ",e)
