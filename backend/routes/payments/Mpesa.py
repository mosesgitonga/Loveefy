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
from models.payment import Subscription, PlanType, TransactionType
import uuid

from services.payments.mpesa import Mpesa
mpesa = Mpesa()

mpesa_bp = Blueprint('mpesa', __name__, url_prefix="/api/mpesa/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@mpesa_bp.route('/stk-push', methods=['POST'], strict_slashes=False)
@jwt_required()
def mpesa_express():
    response = mpesa.stk_push()
    return response 

@mpesa_bp.route('/callback', methods=['POST'], strict_slashes=False)
def mpesa_callback():
    logger.info('callback...')
    try:
        callback_data = request.json
        logger.info("callback data: ", callback_data)

        # Check the result code
        result_code = callback_data['Body']['stkCallback']['ResultCode']
        if result_code != 0:
            # If the result code is not 0, there was an error
            error_message = callback_data['Body']['stkCallback']['ResultDesc']
            response_data = {'ResultCode': result_code, 'ResultDesc': error_message}
            return jsonify(response_data)

        # If the result code is 0, the transaction was completed
        callback_metadata = callback_data['Body']['stkCallback']['CallbackMetadata']
        amount = None
        phone_number = None
        for item in callback_metadata['Item']:
            if item['Name'] == 'Amount':
                amount = item['Value']
            elif item['Name'] == 'PhoneNumber':
                phone_number = item['Value']

        transaction_date = next(item['Value'] for item in callback_metadata if item['Name'] == 'TransactionDate')
        phone_number = next(item['Value'] for item in callback_metadata if item['Name'] == 'PhoneNumber')

        transaction_date = datetime.strptime(str(transaction_date), '%Y%m%d%H%M%S')

 

        if 1 <= amount < 350:
            plan_type = PlanType.PREMIUM
            expiration_days = 7
        elif 350 <= amount < 450:
            plan_type = PlanType.ELITE
            expiration_days = 21
        elif amount >= 450:
            plan_type = PlanType.ELITE
            expiration_days = 30
        else:
            return jsonify({'message': 'Invalid amount received from M-Pesa'}), 400

        new_subscription = Subscription(
            id=str(uuid.uuid4()),
            user_id="332",
            plan_type=plan_type,
            transaction_type=TransactionType.UPGRADE,
            start_date=datetime.utcnow(),
            expiration_date=datetime.utcnow() + timedelta(days=expiration_days),
            transaction_date=transaction_date
        )

        storage = DbStorage()
        storage.new(new_subscription)
        storage.save()

        return jsonify({'message': 'Subscription updated successfully'}), 200

    except Exception as e:
        logger.error(e)
        return jsonify({'message': 'Error processing M-Pesa callback'}), 500
