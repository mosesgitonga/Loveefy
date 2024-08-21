from flask import Flask, request, jsonify
import requests
import base64
from datetime import datetime 
import logging
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os

load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import hashlib

class Mpesa:
    def __init__(self):
        self.LIPA_NG_URL = os.getenv('LIPA_NG_URL')
        self.CONSUMER_KEY = os.getenv('CONSUMER_KEY')
        self.CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
        self.BusinessShortCode = os.getenv('BusinessShortCode')
        self.LipaNaMpesaOnlinePasskey = os.getenv('LipaNaMpesaOnlinePasskey')
        self.Base_URL = os.getenv('Base_URL')
        self.EXPOSED_DEV_URL=os.getenv('EXPOSED_DEVELOPMENT_URL')

    def generate_token(self):
        url = f"{self.Base_URL}/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(url, auth=HTTPBasicAuth(self.CONSUMER_KEY, self.CONSUMER_SECRET))
        return response.json()['access_token']

    def generate_password(self, timestamp):
        data_to_encode = f"{self.BusinessShortCode}{self.LipaNaMpesaOnlinePasskey}{timestamp}"
        encoded_string = base64.b64encode(data_to_encode.encode())
        return encoded_string.decode('utf-8')

    def stk_push(self):
        try:
            data = request.json
            phone_number = data.get('phone_number')
            amount = data.get('amount')
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            password = self.generate_password(timestamp)
            access_token = self.generate_token()

            headers = {
                'Authorization': 'Bearer ' + access_token,
                'Content-Type': 'application/json'
            }

            payload = {
                "BusinessShortCode": self.BusinessShortCode,
                "Password": password,
                "Timestamp": timestamp,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,
                "PartyA": phone_number,
                "PartyB": self.BusinessShortCode,  # Use the correct shortcode
                "PhoneNumber": phone_number,
                "CallBackURL": f"{self.EXPOSED_DEV_URL}/api/mpesa/callback",
                "AccountReference": "loveefy.com",
                "TransactionDesc": "Loveefy Payments"
            }

            response = requests.post(self.LIPA_NG_URL, json=payload, headers=headers)
            response.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
            return jsonify(response.json())
        except Exception as e:
            logger.error(e)
            return jsonify({'message': 'Internal Server Error'}), 500
