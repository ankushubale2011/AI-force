# Selenium-Python Functional Test Suite

This directory contains the **Selenium-Python functional test scripts** generated from the requirements in `1773640130968/Requirement_1.csv`.

## Requirements Covered
- Requirement_1004: Reports and Dashboard section access
- Requirement_1005: Data Genie Landing Page validation
- Requirement_1006: Data Genie search functionality
- Remaining requirements as per `Requirement_1.csv`

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/ankushubale2011/AI-force.git
cd AI-force/tests/selenium/
```

### 2. Set Up Python Environment
Ensure you have **Python 3.x** installed.
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install Dependencies
Install Selenium and any required libraries.
```bash
pip install selenium
```

If testing with Chrome, also install the latest **ChromeDriver**:
- Download from: https://sites.google.com/chromium.org/driver/
- Ensure it's in your system PATH.

### 4. Running the Tests
Each test script corresponds to a requirement and can be run individually:
```bash
python Requirement_1004.py
python Requirement_1005.py
python Requirement_1006.py
```

Or run all tests using unittest discovery:
```bash
python -m unittest discover -s . -p "*.py"
```

### 5. Notes
- Update application URLs and test credentials inside each script.
- Ensure browsers and drivers are properly configured.
- Extend scripts for additional browsers in your test config.

---
**Maintainers:** ankushubale2011

