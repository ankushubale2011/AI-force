import datetime
import json

# Constants
SURVEY_FILE = 'surveys.json'
CUSTOMER_FILE = 'customers.json'
STATUS_PENDING = 'Pending'
STATUS_APPROVED = 'Approved'
STATUS_REJECTED = 'Rejected'
STATUS_COMPLETED = 'Completed'

# Exception Handling
class SurveyException(Exception):
    pass

class CustomerException(Exception):
    pass

# Utility Functions
def load_data(file_path):
    """
    Load data from a JSON file.

    :param file_path: Path to the JSON file.
    :return: Data loaded from the file.
    """
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except Exception as e:
        raise SurveyException(f"Error loading data from {file_path}: {e}")

def save_data(file_path, data):
    """
    Save data to a JSON file.

    :param file_path: Path to the JSON file.
    :param data: Data to be saved.
    """
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        raise SurveyException(f"Error saving data to {file_path}: {e}")

# Survey Management
class Survey:
    def __init__(self, title, questions, start_date, end_date, customer_ids):
        """
        Initialize a new survey.

        :param title: Title of the survey.
        :param questions: List of survey questions.
        :param start_date: Start date of the survey.
        :param end_date: End date of the survey.
        :param customer_ids: List of customer IDs to whom the survey is assigned.
        """
        self.title = title
        self.questions = questions
        self.start_date = start_date
        self.end_date = end_date
        self.customer_ids = customer_ids
        self.status = STATUS_PENDING
        self.responses = {}

    def to_dict(self):
        """
        Convert the survey object to a dictionary.

        :return: Dictionary representation of the survey.
        """
        return self.__dict__

    @staticmethod
    def from_dict(data):
        """
        Create a survey object from a dictionary.

        :param data: Dictionary containing survey data.
        :return: Survey object.
        """
        survey = Survey(
            data['title'],
            data['questions'],
            data['start_date'],
            data['end_date'],
            data['customer_ids']
        )
        survey.status = data['status']
        survey.responses = data['responses']
        return survey

# Lead Manager Functions
def create_survey():
    """
    Create a new survey and save it to the data store.
    """
    try:
        title = input("Enter survey title: ")
        questions = input("Enter survey questions (comma-separated): ").split(',')
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        customer_ids = input("Enter customer IDs (comma-separated): ").split(',')

        survey = Survey(title, questions, start_date, end_date, customer_ids)
        surveys = load_data(SURVEY_FILE)
        surveys.append(survey.to_dict())
        save_data(SURVEY_FILE, surveys)
        print("Survey created successfully.")
    except Exception as e:
        print(f"Error creating survey: {e}")

# CoE Functions
def review_surveys():
    """
    Review pending surveys and update their status based on CoE action.
    """
    try:
        surveys = load_data(SURVEY_FILE)
        for i, survey_data in enumerate(surveys):
            survey = Survey.from_dict(survey_data)
            if survey.status == STATUS_PENDING:
                print(f"Survey {i+1}: {survey.title}")
                print(f"Questions: {', '.join(survey.questions)}")
                print(f"Start Date: {survey.start_date}")
                print(f"End Date: {survey.end_date}")
                action = input("Approve (A), Reject (R), or Request Changes (C): ").upper()
                if action == 'A':
                    survey.status = STATUS_APPROVED
                elif action == 'R':
                    survey.status = STATUS_REJECTED
                elif action == 'C':
                    survey.status = STATUS_PENDING
                else:
                    print("Invalid action.")
                surveys[i] = survey.to_dict()
        save_data(SURVEY_FILE, surveys)
    except Exception as e:
        print(f"Error reviewing surveys: {e}")

# Customer Functions
def take_survey(customer_id):
    """
    Allow a customer to take an approved survey and submit their responses.

    :param customer_id: ID of the customer taking the survey.
    """
    try:
        surveys = load_data(SURVEY_FILE)
        for i, survey_data in enumerate(surveys):
            survey = Survey.from_dict(survey_data)
            if survey.status == STATUS_APPROVED and customer_id in survey.customer_ids:
                print(f"Survey {i+1}: {survey.title}")
                responses = {}
                for question in survey.questions:
                    response = input(f"{question}: ")
                    responses[question] = response
                survey.responses[customer_id] = responses
                survey.status = STATUS_COMPLETED
                surveys[i] = survey.to_dict()
        save_data(SURVEY_FILE, surveys)
    except Exception as e:
        print(f"Error taking survey: {e}")

# Main Function
def main():
    """
    Main function to handle user interaction and role-based actions.
    """
    try:
        while True:
            print("1. Create Survey (Lead Manager)")
            print("2. Review Surveys (CoE)")
            print("3. Take Survey (Customer)")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                create_survey()
            elif choice == '2':
                review_surveys()
            elif choice == '3':
                customer_id = input("Enter your customer ID: ")
                take_survey(customer_id)
            elif choice == '4':
                break
            else:
                print("Invalid choice.")
    except Exception as e:
        print(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
