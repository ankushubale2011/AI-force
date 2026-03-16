package com.example.tests;

import io.qameta.allure.*;
import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.support.ui.ExpectedConditions;

import java.util.List;

@Epic("Dashboard and Reports Testing")
@Feature("ReportsDashboard")
public class ReportsDashboardTest extends BaseTest {

    @Test
    @Description("Validate Reports and Dashboard section functionality including checking existing and new reports.")
    @Severity(SeverityLevel.CRITICAL)
    public void testAccessReportsAndDashboard() {
        login();
        navigateToReportsDashboard();
        verifyCurrentReports();
        checkAndValidateNewReports();
    }

    @Step("Log in to the application")
    private void login() {
        driver.get("https://yourapplication.com/login");
        driver.findElement(By.id("username")).sendKeys("admin");
        driver.findElement(By.id("password")).sendKeys("password123");
        driver.findElement(By.id("loginButton")).click();
    }

    @Step("Navigate to Reports & Dashboard section")
    private void navigateToReportsDashboard() {
        driver.findElement(By.linkText("Reports & Dashboard")).click();
        wait.until(ExpectedConditions.visibilityOfElementLocated(By.id("reportsSection")));
    }

    @Step("Verify current reports and dashboards are available")
    private void verifyCurrentReports() {
        Assertions.assertFalse(driver.findElements(By.cssSelector(".report-item")).isEmpty(),
                "No reports available in the section.");
    }

    @Step("Check if new reports or dashboards are present and validate functionality")
    private void checkAndValidateNewReports() {
        List<WebElement> newReportIcons = driver.findElements(By.cssSelector(".new-report-icon"));
        if (!newReportIcons.isEmpty()) {
            newReportIcons.get(0).click();
            Assertions.assertTrue(driver.findElement(By.id("reportContent")).isDisplayed(),
                    "New report content is not displayed.");
        } else {
            System.err.println("No new reports found. Raise defect for missing reports.");
            Assertions.fail("Missing expected new reports/dashboards.");
        }
    }
}
