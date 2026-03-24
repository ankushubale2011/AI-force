# Test Script Generation Workflow Documentation

This document archives the setup process of the **Test Script Generation** workflow.

## Steps Overview

### 1. Reading Requirements File
- **File:** `/aiforce/assets/data/uploaded_data/1339/Test cases/DMS_20260324_054640_065359/Requirement_1.csv`
- The file contains functional requirements for:
  - **Requirement 1004:** Access to Reports and Dashboard section
  - **Requirement 1005:** Access to Data Genie landing page

### 2. Generating Test Scripts
- Scripts created in **JUnit-style JavaScript**.
- Tools used:
  - **Selenium WebDriver** for automation
  - Mocha/Jest-style syntax for test structuring
- Each requirement mapped to a separate `describe` block with multiple `test` cases.

#### Requirement 1004 Script:
[View in repository](https://github.com/ankushubale2011/AI-force/blob/main/test%20script)

#### Requirement 1005 Script:
[View in repository](https://github.com/ankushubale2011/AI-force/blob/main/test%20script)

### 3. Pushing Scripts to GitHub
- Repository: `ankushubale2011/AI-force`
- Branch: `main`
- File Name: `test script`
- Commit message: *Add JUnit-style JavaScript test scripts for Requirements 1004 and 1005 based on Requirement_1.csv*
- [Commit Link](https://github.com/ankushubale2011/AI-force/commit/c99dcbf3051aa12f243de3054e0ce48333652da3)

### 4. Creating GitHub Actions Workflow
- Workflow file path: `.github/workflows/test.yml`
- Purpose: Automatically runs "test script" file on every commit.
- Environment: `ubuntu-latest`
- Node.js version: `16.x`
- Dependencies:
  - Selenium WebDriver
  - Jest/Mocha
- Trigger: On `push` and `pull_request` to `main`

[View Workflow file](https://github.com/ankushubale2011/AI-force/blob/main/.github/workflows/test.yml)

- Commit message: *Create GitHub Action workflow to automatically run 'test script' on every commit*
- [Commit Link](https://github.com/ankushubale2011/AI-force/commit/4478e6cba7d847255cd63b6c0b0a6e71e7d71687)

## Workflow Benefits
- Automated validation of requirements.
- Continuous integration ensures defects are caught early.
- Single source of truth for test scripts and execution.

---
*Document created for internal archiving purposes.*
