"""
Automated Test Script for UI-Only Login Validation
Language: Python
Framework: Selenium
Author: Test Script Generation Agent
"""

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LoginUITest(unittest.TestCase):
    def setUp(self):
        """Setup selenium driver before each test."""
        self.driver = webdriver.Chrome()  # Assumes chromedriver is installed
        self.driver.maximize_window()
        self.base_url = "http://example.com"  # Replace with actual app URL

    def test_login_ui_only(self):
        driver = self.driver
        try:
            # Step 1: Open application UI
            driver.get(self.base_url)
            logging.info("Opened application UI.")

            # Step 2: Enter valid credentials and log in
            driver.find_element(By.ID, "username").send_keys("validUser")
            driver.find_element(By.ID, "password").send_keys("validPass")
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(2)

            # Step 3: Verify welcome message or profile icon
            self.assertTrue(driver.find_element(By.ID, "welcomeMsg").is_displayed(), "Welcome message not displayed.")
            logging.info("Welcome message displayed.")

            # Step 4: Verify navigation to dashboard/home
            self.assertEqual(driver.current_url, f"{self.base_url}/dashboard", "Did not navigate to dashboard.")
            logging.info("Navigation to dashboard verified.")

            # Step 5: Attempt login with invalid credentials
            driver.get(self.base_url)
            driver.find_element(By.ID, "username").send_keys("invalidUser")
            driver.find_element(By.ID, "password").send_keys("invalidPass")
            driver.find_element(By.ID, "loginBtn").click()
            time.sleep(2)

            # Step 6: Verify error message is displayed
            self.assertTrue("Invalid credentials" in driver.page_source, "Error message not displayed.")
            logging.info("Invalid login error message verified.")

            # Step 7: Confirm no navigation on failed login
            self.assertEqual(driver.current_url, self.base_url, "Unexpected navigation after failed login.")
            logging.info("UI remains on login page after failed login.")
        
        except Exception as e:
            logging.error(f"Exception during test: {e}")
            self.fail(f"Test failed due to exception: {e}")

    def tearDown(self):
        """Close browser after each test."""
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()