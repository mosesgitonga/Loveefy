from flask import Flask, request, jsonify 
from flask_jwt_extended import get_jwt_identity 
import requests
import base64
from datetime import datetime, timedelta
import logging
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from models.engine.DBStorage import DbStorage
from models.payment import Subscription
import uuid

load_dotenv()


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


import hashlib

class Mpesa:
    def __init__(self):
        self.storage = DbStorage()
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

    def stk_push(self, data):
        try:
            phone_number = data.get('phone_number')
            amount = data.get('amount')
            logger.info(phone_number)
            logger.info(amount)
            

            if not phone_number or not amount:
                return jsonify({'message': 'Phone number and amount are required'}), 400

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
                "PartyB": self.BusinessShortCode,
                "PhoneNumber": phone_number,
                "CallBackURL": "https://5cbc-154-159-237-15.ngrok-free.app/api/mpesa/callback",
                "AccountReference": "loveefy",
                "TransactionDesc": "LoveefyPlan"
            }

            response = requests.post(self.LIPA_NG_URL, json=payload, headers=headers)

            if response.status_code == 200:
                logger.info("STK push initiated successfully.")
                return jsonify({'message': 'STK push initiated successfully', 'response': response.json()}), 200
            else:
                response.raise_for_status()

        except Exception as e:
            logger.error(e)
            return jsonify({'message': 'Internal Server Error'}), 500
