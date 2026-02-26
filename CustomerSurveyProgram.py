import uuid
import datetime
from typing import List, Dict, Optional

# ==========================
# Constants & Static Values
# ==========================
SURVEY_STATUS_DRAFT = "Draft"
SURVEY_STATUS_REVIEW = "Under Review"
SURVEY_STATUS_APPROVED = "Approved"
SURVEY_STATUS_REJECTED = "Rejected"
SURVEY_STATUS_PUBLISHED = "Published"
SURVEY_STATUS_COMPLETED = "Completed"

NOTIFICATION_EMAIL_SUBJECT = "New Survey Notification"
EXPORT_FILE_PATH = "./survey_report.csv"

# =================
# Helper Functions
# =================
def generate_unique_id() -> str:
    """Generate a unique ID for objects."""
    try:
        return str(uuid.uuid4())
    except Exception as e:
        raise RuntimeError(f"Error generating unique ID: {e}")

def current_timestamp() -> datetime.datetime:
    """Return the current timestamp."""
    try:
        return datetime.datetime.now()
    except Exception as e:
        raise RuntimeError(f"Error getting current timestamp: {e}")

# =================
# Data Models
# =================
class Survey:
    """Represents a customer survey."""
    
    def __init__(self, title: str, questions: List[str], 
                 customer_id: str, start_date: datetime.date, 
                 end_date: datetime.date):
        try:
            self.survey_id = generate_unique_id()
            self.title = title
            self.questions = questions
            self.customer_id = customer_id
            self.start_date = start_date
            self.end_date = end_date
            self.status = SURVEY_STATUS_DRAFT
            self.responses: Dict[str, str] = {}
            self.audit_trail: List[str] = []
            self.created_at = current_timestamp()
        except Exception as e:
            raise RuntimeError(f"Error initializing Survey: {e}")
    
    def add_audit_log(self, log: str):
        """Add log entry to audit trail."""
        try:
            timestamped_log = f"{current_timestamp()} - {log}"
            self.audit_trail.append(timestamped_log)
        except Exception as e:
            raise RuntimeError(f"Error adding audit log: {e}")

# =================
# Role Classes
# =================
class LeadManager:
    """Lead Manager role: creates and submits surveys for review."""

    def create_survey(self, title: str, questions: List[str], customer_id: str,
                      start_date: datetime.date, end_date: datetime.date) -> Survey:
        """Create a new survey."""
        try:
            survey = Survey(title, questions, customer_id, start_date, end_date)
            survey.add_audit_log("Survey created by Lead Manager.")
            return survey
        except Exception as e:
            raise RuntimeError(f"Error creating survey: {e}")

    def submit_for_review(self, survey: Survey):
        """Submit survey to CoE for review."""
        try:
            survey.status = SURVEY_STATUS_REVIEW
            survey.add_audit_log("Survey submitted for CoE review.")
        except Exception as e:
            raise RuntimeError(f"Error submitting survey for review: {e}")


class CenterOfExcellence:
    """CoE role: reviews and approves/rejects surveys."""

    def review_survey(self, survey: Survey, decision: str):
        """Review survey and take action."""
        try:
            if decision == SURVEY_STATUS_APPROVED:
                survey.status = SURVEY_STATUS_APPROVED
                survey.add_audit_log("Survey approved by CoE.")
            elif decision == SURVEY_STATUS_REJECTED:
                survey.status = SURVEY_STATUS_REJECTED
                survey.add_audit_log("Survey rejected by CoE.")
            else:
                raise ValueError("Invalid decision provided.")
        except Exception as e:
            raise RuntimeError(f"Error reviewing survey: {e}")

    def publish_survey(self, survey: Survey):
        """Publish survey after approval."""
        try:
            if survey.status != SURVEY_STATUS_APPROVED:
                raise RuntimeError("Survey must be approved before publishing.")
            survey.status = SURVEY_STATUS_PUBLISHED
            survey.add_audit_log("Survey published by CoE.")
            self.notify_customer(survey)
        except Exception as e:
            raise RuntimeError(f"Error publishing survey: {e}")

    def notify_customer(self, survey: Survey):
        """Send notification to the customer."""
        try:
            # Simulated notification
            survey.add_audit_log(
                f"Notification sent to customer {survey.customer_id}."
            )
        except Exception as e:
            raise RuntimeError(f"Error notifying customer: {e}")


class Customer:
    """Customer role: completes surveys."""

    def fill_survey(self, survey: Survey, responses: Dict[str, str]):
        """Fill survey responses."""
        try:
            for question, answer in responses.items():
                if question in survey.questions:
                    survey.responses[question] = answer
                else:
                    raise ValueError(f"Invalid question: {question}")
            survey.add_audit_log("Customer filled in survey responses.")
        except Exception as e:
            raise RuntimeError(f"Error filling survey: {e}")

    def submit_survey(self, survey: Survey):
        """Submit survey after filling."""
        try:
            survey.status = SURVEY_STATUS_COMPLETED
            survey.add_audit_log("Customer submitted completed survey.")
        except Exception as e:
            raise RuntimeError(f"Error submitting survey: {e}")

# =================
# Reporting Module
# =================
def export_survey_report(surveys: List[Survey]):
    """Export survey data to CSV file."""
    try:
        import csv
        with open(EXPORT_FILE_PATH, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Survey ID", "Title", "Status", "Customer ID"])
            for survey in surveys:
                writer.writerow([
                    survey.survey_id, survey.title, survey.status,
                    survey.customer_id
                ])
    except Exception as e:
        raise RuntimeError(f"Error exporting survey report: {e}")


# =================
# Example Execution Flow
# =================
if __name__ == "__main__":
    try:
        lm = LeadManager()
        coe = CenterOfExcellence()
        cust = Customer()

        survey = lm.create_survey(
            title="Customer Feedback",
            questions=["Service Quality", "Product Satisfaction"],
            customer_id="CUST123",
            start_date=datetime.date.today(),
            end_date=datetime.date.today() + datetime.timedelta(days=7)
        )
        lm.submit_for_review(survey)
        coe.review_survey(survey, SURVEY_STATUS_APPROVED)
        coe.publish_survey(survey)

        cust.fill_survey(survey, {
            "Service Quality": "Excellent",
            "Product Satisfaction": "High"
        })
        cust.submit_survey(survey)

        export_survey_report([survey])
    except Exception as main_e:
        raise RuntimeError(f"Workflow execution error: {main_e}")