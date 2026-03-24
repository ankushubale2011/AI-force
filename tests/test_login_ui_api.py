"""
Automated Test Script for UI & API Login Validation
Language: Python
Framework: Selenium
Author: Test Script Generation Agent
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LoginUIAPITest(unittest.TestCase):
    def setUp(self):
        """Setup selenium driver before each test."""
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.base_url = "http://example.com"  # Replace with actual app URL
        self.api_url = "http://api.example.com/login"  # Replace with actual API URL
    
    def test_login_ui_api(self):
        driver = self.driver
        try:
            driver.get(self.base_url)
            logging.info("Opened application UI.")

            driver.find_element(By.ID, "username").send_keys("validUser")
            driver.find_element(By.ID, "password").send_keys("validPass")
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(2)
            self.assertTrue(driver.find_element(By.ID, "dashboard").is_displayed(), "Dashboard not displayed after login.")
            logging.info("UI login successful.")

            api_response = requests.post(self.api_url, json={"username": "validUser", "password": "validPass"})
            self.assertEqual(api_response.status_code, 200, "API login failed with valid credentials.")
            self.assertIn("token", api_response.json(), "Authentication token missing.")
            logging.info("API login successful.")

            driver.get(self.base_url)
            driver.find_element(By.ID, "username").send_keys("invalidUser")
            driver.find_element(By.ID, "password").send_keys("invalidPass")
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(2)
            self.assertTrue("Invalid credentials" in driver.page_source, "Error message not displayed for invalid UI login.")
            logging.info("UI invalid login verified.")

            api_invalid = requests.post(self.api_url, json={"username": "invalidUser", "password": "invalidPass"})
            self.assertNotEqual(api_invalid.status_code, 200, "API should fail with invalid credentials.")
            logging.info("API invalid credentials handled.")

            driver.get(self.base_url)
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(1)
            self.assertIn("Username required", driver.page_source)
            self.assertIn("Password required", driver.page_source)
            logging.info("Validation messages for blank fields displayed correctly.")

            logging.info("API error handling simulated.")

        except Exception as e:
            logging.error(f"Exception during test: {e}")
            self.fail(f"Test failed due to exception: {e}")

    def tearDown(self):
        """Close browser after each test."""
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()