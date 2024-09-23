from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging
from datetime import datetime, timedelta
import uuid

from models.engine.DBStorage import DbStorage
from models.payment import Subscription
from services.payments.mpesa import Mpesa

mpesa = Mpesa()
storage = DbStorage()

mpesa_bp = Blueprint('mpesa', __name__, url_prefix="/api/mpesa/")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def save_subscription(subscription):
    """Save subscription to the database."""
    try:
        storage.new(subscription)
        storage.save()
    except Exception as e:
        logger.error(f"An error occurred while saving subscription: {e}")
        raise

@mpesa_bp.route('/stk-push', methods=['POST'], strict_slashes=False)
@jwt_required()
def mpesa_express():
    data = request.json
    phone_number = data.get('phone_number')
    amount = data.get('amount')
    subscription_type = data.get('subscription_type')
    user_id = get_jwt_identity()

    if not phone_number or not subscription_type:
        return jsonify({"status": "failed", "message": "Missing required fields"}), 400

    try:
        amount = int(float(amount))
        if amount < 1:
            return jsonify({"status": "failed", "message": "Invalid amount"}), 400
    except (TypeError, ValueError):
        return jsonify({"status": "failed", "message": "Amount should be a valid number"}), 400

    logger.info(f"STK Push Data: {data}")

    # Initiate STK Push
    payment_response, status_code = mpesa.stk_push(data)
    response_data = payment_response.get_json()

    if response_data.get('response', {}).get('ResponseCode') == '0':
        transaction_id = response_data['response'].get('CheckoutRequestID')

        try:
            existing_subscription = storage.get(Subscription, user_id=user_id)
            if existing_subscription:
                existing_subscription.transaction_type = "Upgrade"
                existing_subscription.amount = amount
                existing_subscription.plan_type = subscription_type
                existing_subscription.transaction_id = transaction_id
                existing_subscription.phone_number = phone_number
                save_subscription(existing_subscription)
            else:
                new_subscription = Subscription(
                    id=uuid.uuid4(),
                    user_id=user_id,
                    phone_number=phone_number,
                    transaction_id=transaction_id,
                    transaction_type=subscription_type,
                    plan_type="GOLD",
                    amount=amount,
                    transaction_date=datetime.now(),
                    status='pending'
                )
                save_subscription(new_subscription)

            return jsonify({"status": "pending", "message": "Check your phone for the Mpesa request"})
        except Exception as e:
            return jsonify({"status": "failed", "message": "An error occurred. Do not pay when prompted"}), 500

    return jsonify({"status": "failed", "message": "Failed to initiate payment"}), 400

@mpesa_bp.route('/callback', methods=['POST'], strict_slashes=False)
def mpesa_callback():
    data = request.json
    result_code = data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
    transaction_id = data.get("Body", {}).get("stkCallback", {}).get("CheckoutRequestID")

    if not transaction_id:
        logger.error("Missing CheckoutRequestID in callback data")
        return jsonify({"status": "error", "message": "Invalid payload"}), 400

    subscription = storage.get(Subscription, transaction_id=transaction_id)
    if subscription:
        if result_code == 0:
            subscription.status = 'successful'
            subscription.expiration_date = datetime.now() + timedelta(days=28)
        else:
            subscription.status = 'failed'
        save_subscription(subscription)
    
    return jsonify({"status": "success" if result_code == 0 else "failed"})
