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
public class DataGenieLandingPageTest {

    private WebDriver driver;
    private WebDriverWait wait;

    @BeforeEach
    public void setUp() {
        driver = new ChromeDriver();
        wait = new WebDriverWait(driver, Duration.ofSeconds(10));
    }

    @Test
    public void testDataGenieLandingPageElements() {
        try {
            driver.get("http://application-url/datagenie");
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.tagName("body")));

            for (WebElement link : driver.findElements(By.tagName("a"))) {
                String href = link.getAttribute("href");
                assertNotNull(href, "Link missing href");
                assertDoesNotThrow(() -> {
                    link.click();
                    driver.navigate().back();
                }, "Link click failed: " + href);
            }

            for (WebElement img : driver.findElements(By.tagName("img"))) {
                String src = img.getAttribute("src");
                assertNotNull(src, "Image missing src");
            }

            assertTrue(driver.findElement(By.tagName("body")).getAttribute("innerHTML").contains("layout"), "Layout missing");

            driver.manage().window().setSize(new Dimension(800, 600));
            assertTrue(driver.findElement(By.tagName("body")).isDisplayed());

            assertTrue(driver.manage().timeouts().getPageLoadTimeout().compareTo(Duration.ofSeconds(5)) <= 0, "Page load slow");

            driver.findElement(By.tagName("body")).sendKeys(Keys.TAB);

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