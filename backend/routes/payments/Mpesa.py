from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
import requests
import base64
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import os
from models.engine.DBStorage import DbStorage
from models.payment import Subscription
from models.engine.DBStorage import DbStorage
import uuid

from services.payments.mpesa import Mpesa
mpesa = Mpesa()
storage = DbStorage()

mpesa_bp = Blueprint('mpesa', __name__, url_prefix="/api/mpesa/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mpesa_bp.route('/stk-push', methods=['POST'], strict_slashes=False)
@jwt_required()
def mpesa_express():
    data = request.json
    phone_number = data.get('phone_number')
    amount = data.get('amount')
    subscription_type = data.get('subscription_type')
    user_id = get_jwt_identity()  # Get user identity once

    if not amount:
        return jsonify({"status": "failed", "message": "Amount is required"}), 400
    
    amount = int(float(amount))
    if amount < 1:
        return jsonify({"status": "failed", "message": "Invalid amount"}), 400

    subscription_plan = 'GOLD'
    
    # Log the incoming data
    logger.info(f"STK Push Data: {data}")
    
    # Initiate STK Push
    payment_response, status_code = mpesa.stk_push(data)
    response_data = payment_response.get_json()
    
    if response_data.get('response', {}).get('ResponseCode') == '0':
        transaction_id = response_data.get('response', {}).get('CheckoutRequestID')
        
        # Save the subscription as pending
        try:
            existing_subscription = storage.get(Subscription, user_id=user_id)
            if existing_subscription:
                existing_subscription.transaction_type = "Upgrade"
                existing_subscription.amount = amount
                existing_subscription.plan_type = subscription_type
                existing_subscription.transaction_id = transaction_id
                existing_subscription.status = "pending"
                existing_subscription.phone_number = phone_number
                storage.new(existing_subscription)
                storage.save()
                return jsonify({"status": "pending", "message": "Check your phone for the Mpesa request"})

            new_subscription = Subscription(
                id=uuid.uuid4(),
                user_id=user_id,
                phone_number=phone_number,
                transaction_id=transaction_id,
                transaction_type=subscription_type,
                plan_type=subscription_plan,
                amount=amount,
                transaction_date=datetime.now(),
                status='pending'
            )
            storage.new(new_subscription)
            storage.save()
            return jsonify({"status": "pending", "message": "Check your phone for the Mpesa request"})

        except Exception as e:
            logger.error(f"An error occurred while saving subscription: {e}")
            return jsonify({"status": "failed", "message": "An error occurred. Do not pay when prompted"}), 400

    return jsonify({"status": "failed", "message": "Failed to initiate payment"}), 400


@mpesa_bp.route('/callback', methods=['POST'], strict_slashes=False)
def mpesa_callback():
    data = request.json
    try:
        result_code = data["Body"]["stkCallback"]["ResultCode"]
        transaction_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
    except KeyError as e:
        logger.error(f"Missing key in callback data: {e}")
        return jsonify({"status": "error", "message": "Invalid payload"}), 400
    logger.info(f'result code \n {result_code}')
    if result_code == 0: 
        subscription = storage.get(Subscription, transaction_id=transaction_id)
        if subscription:
            subscription.status = 'successful'
            subscription.expiration_date = datetime.now() + timedelta(days=28)
            storage.new(subscription)
            storage.save()
            return jsonify({"status": "success"})

    subscription = storage.get(Subscription, transaction_id=transaction_id)
    if subscription:
        subscription.status = 'failed'
        storage.new(subscription)
        storage.save()
    
    return jsonify({"status": "failed"})
