import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.List;

public class ReportsDashboardTest {

    @BeforeEach
    void setUp() {
        // Setup code: Launch browser, login to application
        try {
            TestUtils.launchBrowser();
            TestUtils.login("testUser", "testPassword");
        } catch (Exception e) {
            fail("Setup failed: " + e.getMessage());
        }
    }

    @Test
    void testAccessReportsDashboard() {
        try {
            TestUtils.navigateToSection("Reports and Dashboard");
            assertTrue(TestUtils.isSectionAccessible("Reports and Dashboard"), "Reports and Dashboard section should be accessible");

            List<String> currentReports = TestUtils.getReportsList();
            assertNotNull(currentReports, "Current reports list should not be null");

            List<String> newReports = TestUtils.getNewReportsList();
            if (!newReports.isEmpty()) {
                for (String report : newReports) {
                    assertTrue(TestUtils.isReportFunctional(report), "Report should be functional: " + report);
                }
            } else {
                boolean confirmed = TestUtils.confirmWithDevTeam();
                assertTrue(confirmed, "Dev team confirmation is required when no new reports are found.");
            }

        } catch (Exception e) {
            fail("Test failed due to exception: " + e.getMessage());
        }
    }

    @AfterEach
    void tearDown() {
        TestUtils.closeBrowser();
    }
}