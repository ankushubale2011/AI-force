import os
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# ---------------------- Constants ----------------------
DATABASE_URI = 'sqlite:///customer_survey.db'
SURVEY_STATUS_DRAFT = 'Draft'
SURVEY_STATUS_REVIEW = 'Under Review'
SURVEY_STATUS_APPROVED = 'Approved'
SURVEY_STATUS_REJECTED = 'Rejected'
SURVEY_STATUS_PUBLISHED = 'Published'
SURVEY_STATUS_COMPLETED = 'Completed'
EMAIL_NOTIFICATION_ENABLED = True
EMAIL_NOTIFICATION_SENDER = 'no-reply@surveyprogram.com'

# ---------------------- Initialization ----------------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------------- Models ----------------------
class Survey(db.Model):
    """Represents the survey entity in the system."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default=SURVEY_STATUS_DRAFT)
    customer_email = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    questions = db.relationship('Question', backref='survey', lazy=True)


class Question(db.Model):
    """Represents a question within a survey."""
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)


class SurveyResponse(db.Model):
    """Stores customer responses for a survey."""
    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    responses = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# ---------------------- Utility Functions ----------------------
def send_email_notification(recipient_email, subject, body):
    """
    Sends email notification to a recipient.

    Args:
        recipient_email (str): Email address of recipient.
        subject (str): Email subject line.
        body (str): Email body content.

    Returns:
        bool: True if sent successfully, False otherwise.
    """
    try:
        if EMAIL_NOTIFICATION_ENABLED:
            # Placeholder: In real app, integrate with SMTP or email API
            print(f"Sending email to {recipient_email} - Subject: {subject}")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


# ---------------------- Route Handlers ----------------------
@app.route('/survey/create', methods=['POST'])
def create_survey():
    """
    Creates a new survey and saves it in the database.
    Expects JSON with title, description, created_by, customer_email, dates and questions.
    """
    try:
        data = request.get_json()
        new_survey = Survey(
            title=data.get('title'),
            description=data.get('description'),
            created_by=data.get('created_by'),
            customer_email=data.get('customer_email'),
            start_date=datetime.datetime.strptime(data.get('start_date'), "%Y-%m-%d"),
            end_date=datetime.datetime.strptime(data.get('end_date'), "%Y-%m-%d"),
        )
        db.session.add(new_survey)
        db.session.commit()

        for q_text in data.get('questions', []):
            question = Question(text=q_text, survey_id=new_survey.id)
            db.session.add(question)
        db.session.commit()

        return jsonify({"message": "Survey created successfully"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@app.route('/survey/review/<int:survey_id>', methods=['POST'])
def review_survey(survey_id):
    """
    Reviews a survey and updates its status accordingly.
    Expects JSON with status ('Approved', 'Rejected', or 'Under Review').
    """
    try:
        data = request.get_json()
        survey = Survey.query.get_or_404(survey_id)
        survey.status = data.get('status', SURVEY_STATUS_REVIEW)
        db.session.commit()

        if survey.status == SURVEY_STATUS_APPROVED:
            send_email_notification(survey.customer_email, 
                                    "Survey Approved", 
                                    f"Survey '{survey.title}' has been approved.")
        return jsonify({"message": f"Survey status updated to {survey.status}"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


@app.route('/survey/fill/<int:survey_id>', methods=['POST'])
def fill_survey(survey_id):
    """
    Allows a customer to submit survey responses.
    Expects JSON containing responses list.
    """
    try:
        data = request.get_json()
        survey_response = SurveyResponse(
            survey_id=survey_id,
            responses=str(data.get('responses'))
        )
        db.session.add(survey_response)

        survey = Survey.query.get_or_404(survey_id)
        survey.status = SURVEY_STATUS_COMPLETED
        db.session.commit()

        return jsonify({"message": "Survey responses submitted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    except Exception as ex:
        return jsonify({"error": str(ex)}), 500


# ---------------------- Main Entry ----------------------
if __name__ == '__main__':
    if not os.path.exists('customer_survey.db'):
        db.create_all()
    app.run(debug=True)