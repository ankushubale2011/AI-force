import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class DataGenieLandingPageTest {

    @BeforeEach
    void setUp() {
        try {
            TestUtils.launchBrowser();
        } catch (Exception e) {
            fail("Setup failed: " + e.getMessage());
        }
    }

    @Test
    void testLandingPageLinksAndLayout() {
        try {
            TestUtils.navigateToURL("https://datagenie.example.com");

            // Links verification
            assertTrue(TestUtils.areAllLinksClickable(), "All links should be clickable");
            assertTrue(TestUtils.areLinksNavigatingCorrectly(), "Links should navigate to correct pages");

            // Images verification
            assertTrue(TestUtils.areAllImagesLoaded(), "All images should load correctly");

            // Layout validation
            assertTrue(TestUtils.isLayoutConsistent(), "Layout should be consistent and properly aligned");

            // Responsiveness validation
            assertTrue(TestUtils.isResponsiveAcrossDevices(), "Page should be responsive across devices");

            // Load time & console errors
            assertTrue(TestUtils.isFastLoad(), "Page should load quickly");
            assertFalse(TestUtils.hasConsoleErrors(), "No console errors/warnings expected");

            // Accessibility
            assertTrue(TestUtils.isKeyboardAccessible(), "Keyboard accessibility should be ensured");

            // Cross-browser/OS compatibility
            assertTrue(TestUtils.isCrossBrowserCompatible(), "Page should be cross-browser compatible");

        } catch (Exception e) {
            fail("Test failed due to exception: " + e.getMessage());
        }
    }

    @AfterEach
    void tearDown() {
        TestUtils.closeBrowser();
    }
}