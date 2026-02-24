# AI-force Backend (Flask + MongoDB)

This backend implements the requirements from `1771928815747/Code-Gen-Requirement.txt`:

- User registration with email/phone, password (strong policy), and security question
- Login and logout with session handling
- Forgot password validation and sending a reset link (placeholder)
- Save personal information with validation
- Provide top 10 food types for frontend checkbox selection
- Store all user details in MongoDB

## Tech Stack
- Python, Flask
- MongoDB via Flask-PyMongo

## Getting Started

1. Clone the repository and move into the backend directory:

   ```bash
   git clone https://github.com/ankushubale2011/AI-force.git
   cd AI-force/backend
   ```

2. Create and populate your environment file:

   ```bash
   cp .env.example .env
   # then edit .env to set MONGO_URI and FLASK_SECRET_KEY
   ```

3. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
   pip install -r requirements.txt
   ```

4. Run the server:

   ```bash
   python app.py
   ```

The server runs by default on http://localhost:5000

## Environment Variables
- `MONGO_URI`: MongoDB connection string (e.g., `mongodb://localhost:27017/user_db`)
- `FLASK_SECRET_KEY`: Secret key for Flask session cookies

## API Endpoints

- `POST /register`
  - Body: `{ "email_or_phone": "user@domain.com" or "555-555-5555", "password": "Password@123", "confirm_password": "Password@123", "security_question": "..." }`
  - Errors include: `Invalid email address or phone number`, `Passwords do not match`, and password policy message.

- `POST /login`
  - Body: `{ "email_or_phone": "...", "password": "..." }`
  - Errors: `Incorrect email or password`

- `POST /logout`
  - Logs out current session

- `POST /save_personal_info`
  - Body: `{ "name": "John", "age": 30, "sex": "Male", "address": "123 Main St", "profile_picture": "https://..." }`
  - Errors include: `Invalid name`, `Age must be between 18 and 99`, `Invalid sex`, `Invalid address`.

- `GET /food_types`
  - Returns: `{ "food_types": ["Indian", "Chinese", ...] }`

- `POST /forgot_password`
  - Body: `{ "email_or_phone": "...", "security_question": "..." }`
  - Returns: `Password reset link sent` if validation succeeds (placeholder action)

## Notes
- This sample uses regex-based validation and stores password hashes (never store plain text).
- Replace the password reset placeholder with real email/SMS delivery in production.
- Consider adding CORS, rate-limiting, and structured logging for production.
