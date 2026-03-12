import pytest
import time
import os
from CustomerSurveyProgram import (
    generate_unique_id,
    current_timestamp,
    Survey,
    Customer,
    SurveyManager
)


def test_generate_unique_id_positive():
    """Test generate_unique_id returns a unique ID for positive scenario."""
    uid1 = generate_unique_id()
    uid2 = generate_unique_id()
    assert uid1 != uid2
    assert isinstance(uid1, str)
    assert len(uid1) > 0


def test_generate_unique_id_boundary():
    """Test generate_unique_id boundary scenario for uniqueness."""
    ids = [generate_unique_id() for _ in range(1000)]
    assert len(set(ids)) == len(ids)


def test_current_timestamp_positive():
    """Test current_timestamp returns a valid timestamp string."""
    ts = current_timestamp()
    assert isinstance(ts, str)
    assert len(ts) > 0


def test_survey_creation_positive():
    """Test positive creation of a survey."""
    survey = Survey("Service Feedback", "Rate our service")
    assert survey.title == "Service Feedback"
    assert survey.description == "Rate our service"
    assert isinstance(survey.id, str)


def test_survey_submission_positive():
    """Test positive submission of a survey."""
    survey = Survey("Service Feedback", "Rate our service")
    survey.submit()
    assert survey.status == "Submitted"


def test_survey_review_positive():
    """Test positive review of a survey."""
    survey = Survey("Service Feedback", "Rate our service")
    survey.submit()
    survey.review()
    assert survey.status == "Reviewed"


def test_survey_publish_positive():
    """Test positive publishing of a survey."""
    survey = Survey("Service Feedback", "Rate our service")
    survey.submit()
    survey.review()
    survey.publish()
    assert survey.status == "Published"


def test_customer_take_survey_positive():
    """Test positive scenario of a customer taking a survey."""
    survey = Survey("Service Feedback", "Rate our service")
    survey.submit()
    survey.review()
    survey.publish()
    customer = Customer("John Doe")
    customer.take_survey(survey, {"rating": 5, "comments": "Excellent"})
    assert survey.responses[0]['rating'] == 5


def test_survey_manager_add_survey_positive():
    """Test adding a survey to SurveyManager."""
    sm = SurveyManager()
    survey = Survey("Service Feedback", "Rate our service")
    sm.add_survey(survey)
    assert survey in sm.surveys


def test_survey_manager_export_csv_positive(tmp_path):
    """Test CSV export functionality in SurveyManager."""
    sm = SurveyManager()
    survey = Survey("Service Feedback", "Rate our service")
    survey.submit()
    survey.review()
    survey.publish()
    survey.responses.append({"rating": 5, "comments": "Excellent"})
    sm.add_survey(survey)
    csv_file = tmp_path / "report.csv"
    sm.export_surveys_to_csv(str(csv_file))
    assert os.path.exists(csv_file)


def test_performance_generate_unique_id():
    """Performance test for generate_unique_id under load."""
    start_time = time.time()
    for _ in range(10000):
        generate_unique_id()
    end_time = time.time()
    assert (end_time - start_time) < 2


def test_security_survey_data_integrity():
    """Security test to ensure survey data cannot be tampered accidentally."""
    survey = Survey("Service Feedback", "Rate our service")
    original_id = survey.id
    with pytest.raises(AttributeError):
        survey.id = "fake_id"
    assert survey.id == original_id


def test_usability_customer_interaction():
    """Usability test for intuitive survey flow."""
    sm = SurveyManager()
    survey = Survey("Service Feedback", "Rate our service")
    sm.add_survey(survey)
    assert any(s.title == "Service Feedback" for s in sm.surveys)


if __name__ == "__main__":
    pytest.main()