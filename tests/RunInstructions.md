# Run Instructions

This document provides step-by-step guidance to execute the TestNG suite locally.

## Prerequisites
1. **Java Development Kit (JDK)** installed (version 8 or above).
2. **Apache Maven** installed.
3. **Selenium WebDriver** dependency added in your `pom.xml`.
4. **Chrome browser** installed.
5. **chromedriver** downloaded and path configured.

## Setup Steps

### 1. Clone the Repository
```bash
 git clone https://github.com/ankushubale2011/AI-force.git
 cd AI-force
```

### 2. Configure chromedriver Path
Update the scripts (`ReportsDashboardTest.java` and `DataGenieLandingPageTest.java`) with the actual path to your downloaded chromedriver:
```java
System.setProperty("webdriver.chrome.driver", "/path/to/chromedriver");
```

### 3. Update Application URLs
Replace the placeholder URLs (`http://application-url/login` and `http://application-url/datagenie`) with your environment's actual application URLs.

### 4. Install Maven Dependencies
Ensure `pom.xml` contains Selenium and TestNG dependencies:
```xml
<dependency>
    <groupId>org.seleniumhq.selenium</groupId>
    <artifactId>selenium-java</artifactId>
    <version>4.1.2</version>
</dependency>
<dependency>
    <groupId>org.testng</groupId>
    <artifactId>testng</artifactId>
    <version>7.4.0</version>
    <scope>test</scope>
</dependency>
```
Then install them:
```bash
mvn clean install
```

### 5. Run the Test Suite
Use Maven to run the TestNG suite:
```bash
mvn test -DsuiteXmlFile=tests/testng-suite.xml
```

### 6. View Test Results
The results will be available in the `target/surefire-reports` directory. Open the `index.html` file for a detailed report.

---
**Note:** Ensure Chrome and chromedriver versions are compatible.