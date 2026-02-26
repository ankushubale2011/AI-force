import datetime
import uuid
from typing import List, Dict, Optional

# Constants for static values
SURVEY_STORAGE_PATH = "/data/surveys/"
NOTIFICATION_EMAIL_TEMPLATE = "Survey {survey_id} has been published."
STATUS_PENDING_REVIEW = "Pending Review"
STATUS_APPROVED = "Approved"
STATUS_REJECTED = "Rejected"
STATUS_PUBLISHED = "Published"
STATUS_IN_PROGRESS = "In Progress"
STATUS_COMPLETED = "Completed"

# Role constants
ROLE_LEAD_MANAGER = "Lead Manager"
ROLE_COE = "Center of Excellence"
ROLE_CUSTOMER = "Customer"


class Survey:
    """Class representing a survey object."""

    def __init__(self, title: str, questions: List[str], start_date: datetime.date,
                 end_date: datetime.date, customer_id: str):
        self.survey_id = str(uuid.uuid4())
        self.title = title
        self.questions = questions
        self.start_date = start_date
        self.end_date = end_date
        self.customer_id = customer_id
        self.status = STATUS_PENDING_REVIEW
        self.responses = {}
        self.audit_trail = []


class SurveyManager:
    """Manager for survey operations based on user roles."""

    def __init__(self):
        self.surveys: Dict[str, Survey] = {}

    def create_survey(self, title: str, questions: List[str],
                      start_date: datetime.date, end_date: datetime.date,
                      customer_id: str) -> Optional[str]:
        """
        Create a new survey and return its ID.
        """
        try:
            survey = Survey(title, questions, start_date, end_date, customer_id)
            self.surveys[survey.survey_id] = survey
            self._log_action(survey.survey_id, ROLE_LEAD_MANAGER, "Survey Created")
            return survey.survey_id
        except Exception as e:
            print(f"Error creating survey: {e}")
            return None

    def review_survey(self, survey_id: str, role: str, decision: str) -> bool:
        """
        Review survey by CoE and update status.
        Decision can be 'approve', 'reject', or 'request_changes'.
        """
        try:
            survey = self.surveys.get(survey_id)
            if not survey:
                raise ValueError("Survey not found.")

            if role != ROLE_COE:
                raise PermissionError("Unauthorized role for review.")

            if decision.lower() == "approve":
                survey.status = STATUS_APPROVED
            elif decision.lower() == "reject":
                survey.status = STATUS_REJECTED
            elif decision.lower() == "request_changes":
                survey.status = STATUS_PENDING_REVIEW
            else:
                raise ValueError("Invalid decision.")

            self._log_action(survey_id, role, f"Review decision: {decision}")
            return True
        except Exception as e:
            print(f"Error reviewing survey: {e}")
            return False

    def publish_survey(self, survey_id: str) -> bool:
        """
        Publish an approved survey to customers.
        """
        try:
            survey = self.surveys.get(survey_id)
            if not survey:
                raise ValueError("Survey not found.")

            if survey.status != STATUS_APPROVED:
                raise ValueError("Survey is not approved for publish.")

            survey.status = STATUS_PUBLISHED
            self._send_notification_email(survey.survey_id)
            self._log_action(survey_id, ROLE_COE, "Survey Published")
            return True
        except Exception as e:
            print(f"Error publishing survey: {e}")
            return False

    def submit_response(self, survey_id: str, customer_id: str,
                        responses: Dict[str, str], is_final: bool) -> bool:
        """
        Submit or save survey responses for a customer.
        """
        try:
            survey = self.surveys.get(survey_id)
            if not survey:
                raise ValueError("Survey not found.")

            if survey.customer_id != customer_id:
                raise PermissionError("Unauthorized customer.")

            survey.responses[customer_id] = responses
            survey.status = STATUS_COMPLETED if is_final else STATUS_IN_PROGRESS
            self._log_action(survey_id, ROLE_CUSTOMER,
                             "Final Response Submitted" if is_final else "Response Saved")
            return True
        except Exception as e:
            print(f"Error submitting response: {e}")
            return False

    def export_survey_data(self, survey_id: str) -> Optional[Dict[str, any]]:
        """
        Export survey data including responses and audit trail.
        """
        try:
            survey = self.surveys.get(survey_id)
            if not survey:
                raise ValueError("Survey not found.")

            return {
                "survey_id": survey.survey_id,
                "title": survey.title,
                "status": survey.status,
                "responses": survey.responses,
                "audit_trail": survey.audit_trail
            }
        except Exception as e:
            print(f"Error exporting survey data: {e}")
            return None

    def _log_action(self, survey_id: str, role: str, action: str):
        """
        Log an action for audit purposes.
        """
        try:
            survey = self.surveys.get(survey_id)
            timestamp = datetime.datetime.now().isoformat()
            survey.audit_trail.append({
                "role": role,
                "action": action,
                "timestamp": timestamp
            })
        except Exception as e:
            print(f"Error logging action: {e}")

    def _send_notification_email(self, survey_id: str):
        """
        Simulate sending a notification email.
        """
        try:
            message = NOTIFICATION_EMAIL_TEMPLATE.format(survey_id=survey_id)
            print(f"Sending Email: {message}")
        except Exception as e:
            print(f"Error sending notification email: {e}")


# Example usage (for testing only)
if __name__ == "__main__":
    manager = SurveyManager()
    survey_id = manager.create_survey(
        "Customer Satisfaction Survey",
        ["Q1: How satisfied are you?", "Q2: What can we improve?"],
        datetime.date.today(),
        datetime.date.today() + datetime.timedelta(days=7),
        "customer_123"
    )
    manager.review_survey(survey_id, ROLE_COE, "approve")
    manager.publish_survey(survey_id)
    manager.submit_response(survey_id, "customer_123",
                            {"Q1": "Very satisfied", "Q2": "More discount"},
                            is_final=True)
    data = manager.export_survey_data(survey_id)
    print(data)
