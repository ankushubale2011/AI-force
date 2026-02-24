from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import re
import os

# Load environment variables from .env if present (for local/dev)
load_dotenv()

app = Flask(__name__)
# Secret key from env (recommended). Falls back to random for dev if not set.
app.secret_key = os.getenv("FLASK_SECRET_KEY") or os.urandom(24)

# MongoDB configuration from environment
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/user_db")
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# Constants
EMAIL_REGEX = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
PHONE_REGEX = r'^\d{3}-\d{3}-\d{4}$'
PASSWORD_REGEX = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
FOOD_TYPES = [
    "Indian",
    "Chinese",
    "French",
    "Italian",
    "Mexican",
    "Japanese",
    "Thai",
    "American",
    "Greek",
    "Mediterranean",
]

# Utility validation functions
def validate_email(email: str) -> bool:
    return bool(email) and re.match(EMAIL_REGEX, email) is not None


def validate_phone(phone: str) -> bool:
    return bool(phone) and re.match(PHONE_REGEX, phone) is not None


def validate_password(password: str) -> bool:
    return bool(password) and re.match(PASSWORD_REGEX, password) is not None


def validate_name(name: str) -> bool:
    return isinstance(name, str) and len(name) >= 2 and name.isalpha()


def validate_age(age) -> bool:
    try:
        age_val = int(age)
    except (TypeError, ValueError):
        return False
    return 18 <= age_val <= 99


def validate_sex(sex: str) -> bool:
    return sex in ["Male", "Female"]


def validate_address(address: str) -> bool:
    return isinstance(address, str) and len(address) >= 5 and re.match(r'^[a-zA-Z0-9 ]*$', address) is not None


def validate_security_question(security_question: str) -> bool:
    return bool(security_question)


def validate_profile_picture(profile_picture: str) -> bool:
    # Placeholder: in real apps, handle uploads/storage securely
    return bool(profile_picture)


# Routes
@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user with email/phone, password, and security question.
    Body JSON:
    {
      "email_or_phone": "user@domain.com" or "555-555-5555",
      "password": "Password@123",
      "confirm_password": "Password@123",
      "security_question": "Your pet's name?"
    }
    """
    try:
        data = request.get_json(force=True, silent=True) or {}
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        security_question = data.get('security_question')

        if not (validate_email(email_or_phone) or validate_phone(email_or_phone)):
            return jsonify({"error": "Invalid email address or phone number"}), 400
        if not validate_password(password):
            return jsonify({
                "error": "Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one number, and one special character"
            }), 400
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match"}), 400
        if not validate_security_question(security_question):
            return jsonify({"error": "Security question cannot be empty"}), 400

        # Check if user already exists
        existing = mongo.db.users.find_one({"email_or_phone": email_or_phone})
        if existing:
            return jsonify({"error": "User already exists"}), 409

        hashed_password = generate_password_hash(password)
        user = {
            "email_or_phone": email_or_phone,
            "password": hashed_password,
            "security_question": security_question,
        }
        mongo.db.users.insert_one(user)
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/save_personal_info', methods=['POST'])
def save_personal_info():
    """
    Save personal information of the user.
    Body JSON:
    {
      "name": "John",
      "age": 30,
      "sex": "Male",
      "address": "123 Main St",
      "profile_picture": "https://.../avatar.png"
    }
    """
    try:
        data = request.get_json(force=True, silent=True) or {}
        name = data.get('name')
        age = data.get('age')
        sex = data.get('sex')
        address = data.get('address')
        profile_picture = data.get('profile_picture')

        if not validate_name(name):
            return jsonify({"error": "Invalid name"}), 400
        if not validate_age(age):
            return jsonify({"error": "Age must be between 18 and 99"}), 400
        if not validate_sex(sex):
            return jsonify({"error": "Invalid sex"}), 400
        if not validate_address(address):
            return jsonify({"error": "Invalid address"}), 400
        if not validate_profile_picture(profile_picture):
            return jsonify({"error": "Profile picture cannot be empty"}), 400

        personal_info = {
            "name": name,
            "age": int(age),
            "sex": sex,
            "address": address,
            "profile_picture": profile_picture,
        }
        mongo.db.personal_info.insert_one(personal_info)
        return jsonify({"message": "Personal information saved successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/food_types', methods=['GET'])
def food_types():
    """Get the list of top 10 food types."""
    try:
        return jsonify({"food_types": FOOD_TYPES}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    """
    Handle forgot password flow by validating security question and sending reset link.
    Body JSON:
    {
      "email_or_phone": "user@domain.com" or "555-555-5555",
      "security_question": "Your pet's name?"
    }
    """
    try:
        data = request.get_json(force=True, silent=True) or {}
        email_or_phone = data.get('email_or_phone')
        security_question = data.get('security_question')

        user = mongo.db.users.find_one({
            "email_or_phone": email_or_phone,
            "security_question": security_question,
        })
        if not user:
            return jsonify({"error": "Invalid security question answer"}), 400

        # Placeholder for sending a password reset link (email/SMS integration)
        return jsonify({"message": "Password reset link sent"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate user login with email/phone and password.
    Body JSON:
    {
      "email_or_phone": "user@domain.com" or "555-555-5555",
      "password": "Password@123"
    }
    """
    try:
        data = request.get_json(force=True, silent=True) or {}
        email_or_phone = data.get('email_or_phone')
        password = data.get('password')

        user = mongo.db.users.find_one({"email_or_phone": email_or_phone})
        if not user or not check_password_hash(user['password'], password):
            return jsonify({"error": "Incorrect email or password"}), 400

        session['user_id'] = str(user['_id'])
        return jsonify({"message": "Login successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/logout', methods=['POST'])
def logout():
    """Log out the current user."""
    try:
        session.pop('user_id', None)
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # For development use only.
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
