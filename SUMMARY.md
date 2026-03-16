# Project Setup Summary

## 1. Folder Structure
```
project-root/
├── pom.xml                              # Maven config with Selenium, JUnit, Spring Boot, Allure
├── README.md                            # Project description, usage instructions, screenshots
├── SUMMARY.md                           # Setup documentation (this file)
├── src/
│   ├── main/java/com/example/app/        # Spring Boot application code
│   └── test/java/com/example/tests/      # Test classes
│       ├── BaseTest.java                 # Centralized WebDriver setup/teardown
│       ├── ReportsDashboardTest.java     # Tests for Reports & Dashboard section
│       ├── DataGenieLandingPageTest.java # Tests for Data Genie landing page
│   └── test/resources/test-data/         # Requirement_1.csv and other test data
├── docs/screenshots/                     # Allure report screenshots
├── logs/                                 # Execution logs
├── reports/                              # Generated test reports
└── drivers/                              # Browser driver executables
```

## 2. BaseTest Implementation
- Centralizes WebDriver setup/teardown using **WebDriverManager**.
- Provides shared `WebDriver` and `WebDriverWait` instances.
- Extended by all test classes to avoid duplicate setup code.

## 3. Test Scripts Created
### ReportsDashboardTest.java
- Automates login and navigation to Reports & Dashboard.
- Validates existing/new reports presence and functionality.
- Reports defects when missing.

### DataGenieLandingPageTest.java
- Verifies link clickability and correctness.
- Ensures images load properly.
- Checks layout consistency, responsiveness, accessibility, performance.
- Annotated for Allure reporting.

## 4. Allure Integration Details
- Maven dependencies for Allure JUnit 5 integration.
- Configured `allure.results.directory` and `allure.report.directory`.
- Annotated steps in test scripts (`@Description`, `@Step`, `@Severity`).
- Allure reports generated with:
```bash
mvn clean test
mvn allure:serve
```

## 5. GitHub Actions CI/CD Workflow
- Runs Maven tests automatically on each push to `main`.
- Generates Allure results and HTML reports.
- Uploads reports as build artifacts.

## 6. GitHub Pages Deployment Process
- CI/CD workflow deploys `target/allure-report` contents to `gh-pages` branch.
- Reports publicly accessible at:
```
https://ankushubale2011.github.io/AI-force/
```

## 7. README Enhancements
- Added instructions for local test execution.
- Allure report viewing locally and via GitHub Pages.
- Embedded sample screenshots of Allure dashboard and test details.

## 8. Screenshot Additions
- Stored in `docs/screenshots/`.
- Linked in README for visual reference.

---
**This setup now provides complete automated testing, reporting, CI/CD integration, and public accessibility of results.**