package com.example.application.tests;

import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.*;
import org.springframework.boot.test.context.SpringBootTest;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.openqa.selenium.support.ui.ExpectedConditions;
import java.time.Duration;

@SpringBootTest
public class ReportsDashboardAccessTest {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    public void setUp() {
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @Test
    public void testReportsAndDashboardAccess() {
        try {
            driver.get("http://application-url/login");
            driver.findElement(By.id("username")).sendKeys("testuser");
            driver.findElement(By.id("password")).sendKeys("testpassword");
            driver.findElement(By.id("login-button")).click();
            wait.until(ExpectedConditions.urlContains("dashboard"));
            driver.findElement(By.linkText("Reports and Dashboard")).click();

            assertFalse(driver.findElements(By.cssSelector(".report")).isEmpty(), "No reports found");
            assertFalse(driver.findElements(By.cssSelector(".dashboard")).isEmpty(), "No dashboards found");

            boolean newReportsFound = driver.findElements(By.cssSelector(".new-report")).size() > 0;
            boolean newDashboardsFound = driver.findElements(By.cssSelector(".new-dashboard")).size() > 0;

            if (newReportsFound || newDashboardsFound) {
                driver.findElement(By.cssSelector(".new-report")).click();
                assertTrue(driver.getPageSource().contains("Report Details"), "Report details not visible");
            } else {
                fail("No new reports or dashboards added. Please confirm with development team.");
            }
        } catch (Exception e) {
            fail("Exception occurred: " + e.getMessage());
        }
    }

    @AfterEach
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}