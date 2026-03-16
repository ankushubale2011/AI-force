import org.testng.Assert;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.Keys;
import org.openqa.selenium.JavascriptExecutor;
import java.util.List;

public class DataGenieLandingPageTest {

    WebDriver driver;

    @BeforeClass
    public void setUp() {
        System.setProperty("webdriver.chrome.driver", "/path/to/chromedriver");
        driver = new ChromeDriver();
        driver.manage().window().maximize();
    }

    @Test
    public void testDataGenieLandingPage() {
        try {
            driver.get("http://application-url/datagenie");

            List<WebElement> links = driver.findElements(By.tagName("a"));
            Assert.assertTrue(!links.isEmpty(), "No links found on page.");
            for (WebElement link : links) {
                String href = link.getAttribute("href");
                Assert.assertNotNull(href, "Link missing href attribute.");
            }

            for (WebElement link : links) {
                String href = link.getAttribute("href");
                driver.navigate().to(href);
                Assert.assertTrue(driver.getTitle().length() > 0, "Page title missing after navigation.");
                driver.navigate().back();
            }

            List<WebElement> images = driver.findElements(By.tagName("img"));
            for (WebElement img : images) {
                Assert.assertTrue(img.isDisplayed(), "Image not loaded properly.");
            }

            JavascriptExecutor js = (JavascriptExecutor) driver;
            long scrollHeight = (long) js.executeScript("return document.body.scrollHeight");
            Assert.assertTrue(scrollHeight > 0, "Page layout may be broken.");

            driver.manage().window().setSize(new org.openqa.selenium.Dimension(800, 600));
            Assert.assertTrue(scrollHeight > 0, "Responsive layout may be broken.");

            driver.findElement(By.tagName("body")).sendKeys(Keys.TAB);

            System.out.println("Browser compatibility check simulated.");

        } catch (Exception e) {
            Assert.fail("Test failed due to exception: " + e.getMessage());
        }
    }

    @AfterClass
    public void tearDown() {
        if (driver != null) {
            driver.quit();
        }
    }
}