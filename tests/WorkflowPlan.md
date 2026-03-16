# Workflow Plan - Test Script Generation

## 1. Requirements Intake
- Gather requirements file (CSV, Excel, or text) detailing test objectives.
- Confirm testing framework (TestNG) and language (Java Spring Boot).
- Define scope (e.g., functional, regression, UI testing).
- Specify output format and special guidelines.

## 2. Test Script Generation
- Generate scripts based on the requirements file.
- Implement Selenium WebDriver for UI automation.
- Leave placeholders for `chromedriver` path and application URLs.
- Include validation steps, assertions, and exception handling.

## 3. Structured Folder Creation
```
tests/
 ├── reports_dashboard/
 │    ├── ReportsDashboardTest.java
 │    └── README.md
 ├── data_genie/
 │    ├── DataGenieLandingPageTest.java
 │    └── README.md
```
- README.md in each folder includes testing purpose, prerequisites, and execution notes.

## 4. TestNG Suite XML Creation
- Create `tests/testng-suite.xml` file.
- Configure suite to run both `ReportsDashboardTest` and `DataGenieLandingPageTest`.
- Enable suite execution via Maven command:
```bash
mvn test -DsuiteXmlFile=tests/testng-suite.xml
```

## 5. ZIP Packaging
- Prepare a downloadable archive of the `tests/` folder.
- Include all test scripts, README.md files, and suite XML.

## 6. Run Instructions File
- Add `tests/RunInstructions.md` containing:
  - Environment setup (JDK, Maven, Selenium WebDriver)
  - Updating placeholders
  - Running suite via Maven
  - Viewing results

## 7. Repeatability
- This document (`WorkflowPlan.md`) serves as a reference for repeating the process.
- Steps can be re-run anytime by replacing the requirements file and regenerating scripts.

## Notes
- Maintain placeholders until actual paths and URLs are finalized.
- Scripts can be extended with additional verification steps.
- Automation can be expanded to CI/CD if needed in future.
