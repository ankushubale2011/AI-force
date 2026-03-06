import json
import datetime
from typing import List, Dict, Optional

# ===========================
# Constants
# ===========================
SURVEY_STATUS_DRAFT = "DRAFT"
SURVEY_STATUS_PENDING_REVIEW = "PENDING_REVIEW"
SURVEY_STATUS_APPROVED = "APPROVED"
SURVEY_STATUS_REJECTED = "REJECTED"
SURVEY_STATUS_PUBLISHED = "PUBLISHED"
SURVEY_STATUS_COMPLETED = "COMPLETED"

NOTIFICATION_EMAIL_TEMPLATE = "survey_notification_template.html"
AUDIT_LOG_FILE = "audit_log.json"
REPORT_FILE = "survey_report.json"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ===========================
# Utility Functions
# ===========================

def log_audit(action: str, details: dict):
    """Log actions to the audit log file."""
    try:
        log_entry = {
            "timestamp": datetime.datetime.now().strftime(DATE_FORMAT),
            "action": action,
            "details": details
        }
        with open(AUDIT_LOG_FILE, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
    except Exception as e:
        print(f"Failed to write to audit log: {e}")


def send_notification(recipient: str, subject: str, message: str):
    """Simulate sending a notification."""
    try:
        print(f"Sending notification to {recipient} - {subject}")
        # Placeholder for email sending integration via NOTIFICATION_EMAIL_TEMPLATE
    except Exception as e:
        print(f"Notification error: {e}")


# ===========================
# Core Classes
# ===========================

class Survey:
    """Survey entity with status and attributes."""
    def __init__(self, title: str, questions: List[str],
                 customers: List[str], start_date: datetime.datetime,
                 end_date: datetime.datetime):
        self.title = title
        self.questions = questions
        self.customers = customers
        self.start_date = start_date
        self.end_date = end_date
        self.status = SURVEY_STATUS_DRAFT
        self.responses: Dict[str, dict] = {}

    def to_dict(self) -> dict:
        """Convert survey to a dictionary."""
        return {
            "title": self.title,
            "questions": self.questions,
            "customers": self.customers,
            "start_date": self.start_date.strftime(DATE_FORMAT),
            "end_date": self.end_date.strftime(DATE_FORMAT),
            "status": self.status,
            "responses": self.responses
        }


class SurveyManager:
    """Manages survey lifecycle."""
    def __init__(self):
        self.surveys: List[Survey] = []

    def create_survey(self, title: str, questions: List[str],
                      customers: List[str], start_date: datetime.datetime,
                      end_date: datetime.datetime) -> Survey:
        """Create a new survey and log action."""
        try:
            survey = Survey(title, questions, customers, start_date, end_date)
            self.surveys.append(survey)
            log_audit("CREATE_SURVEY", survey.to_dict())
            return survey
        except Exception as e:
            print(f"Error creating survey: {e}")
            raise

    def submit_for_review(self, survey: Survey):
        """Submit survey for CoE review."""
        try:
            survey.status = SURVEY_STATUS_PENDING_REVIEW
            log_audit("SUBMIT_FOR_REVIEW", survey.to_dict())
        except Exception as e:
            print(f"Error in submit_for_review: {e}")

    def review_survey(self, survey: Survey, approve: bool,
                      comments: Optional[str] = None):
        """Review survey and set status."""
        try:
            if approve:
                survey.status = SURVEY_STATUS_APPROVED
            else:
                survey.status = SURVEY_STATUS_REJECTED
            log_audit("REVIEW_SURVEY", {
                "survey": survey.to_dict(),
                "comments": comments
            })
        except Exception as e:
            print(f"Error in review_survey: {e}")

    def publish_survey(self, survey: Survey):
        """Publish approved survey."""
        try:
            if survey.status != SURVEY_STATUS_APPROVED:
                raise ValueError("Survey not approved for publishing.")
            survey.status = SURVEY_STATUS_PUBLISHED
            for cust in survey.customers:
                send_notification(
                    cust, f"Survey Available: {survey.title}",
                    "Please complete the survey before deadline."
                )
            log_audit("PUBLISH_SURVEY", survey.to_dict())
        except Exception as e:
            print(f"Error publishing survey: {e}")

    def submit_response(self, survey: Survey, customer: str,
                        responses: Dict[str, str]):
        """Submit customer survey response."""
        try:
            survey.responses[customer] = responses
            survey.status = SURVEY_STATUS_COMPLETED
            log_audit("SUBMIT_RESPONSE", {
                "survey": survey.title,
                "customer": customer,
                "responses": responses
            })
        except Exception as e:
            print(f"Error submitting response: {e}")

    def export_report(self):
        """Export survey data to file."""
        try:
            report_data = [survey.to_dict() for survey in self.surveys]
            with open(REPORT_FILE, "w") as file:
                json.dump(report_data, file, indent=4)
            log_audit("EXPORT_REPORT", {"file": REPORT_FILE})
        except Exception as e:
            print(f"Error exporting report: {e}")


# ===========================
# Example usage (can be removed in production)
# ===========================

if __name__ == "__main__":
    manager = SurveyManager()
    survey = manager.create_survey(
        "Customer Feedback Q1",
        ["How satisfied are you?", "Any suggestions?"],
        ["customer1@example.com", "customer2@example.com"],
        datetime.datetime.now(),
        datetime.datetime.now() + datetime.timedelta(days=7)
    )
    manager.submit_for_review(survey)
    manager.review_survey(survey, approve=True)
    manager.publish_survey(survey)
    manager.submit_response(
        survey, "customer1@example.com",
        {"Q1": "Very Satisfied", "Q2": "Keep up the good work!"}
    )
    manager.export_report()