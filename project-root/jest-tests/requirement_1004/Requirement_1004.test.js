// Jest Test for Access to Reports and Dashboard section in Java Spring Boot Application

const { loginAndNavigateToReportsDashboard, fetchReportsAndDashboards, verifyReportFunctionality } = require('./Requirement_1004_utilities');

describe('Reports and Dashboard Access', () => {
    test('Verify access and functionality of existing and new reports/dashboards', async () => {
        try {
            await loginAndNavigateToReportsDashboard(); // Step 1

            const reports = await fetchReportsAndDashboards(); // Step 2
            expect(reports).not.toBeNull();
            expect(Array.isArray(reports)).toBe(true);

            const newReports = reports.filter(r => r.isNew); // Step 3
            if (newReports.length > 0) {
                for (const report of newReports) {
                    const result = await verifyReportFunctionality(report); // Step 4
                    expect(result.status).toBe('PASS');
                }
                console.log('New reports verified successfully.');
            } else {
                console.warn('No new reports found. Contact dev team for confirmation.'); // Step 5
                fail('Missing new reports/dashboards - defect logged.');
            }
        } catch (error) {
            console.error('Test failed due to exception:', error);
            fail(error);
        }
    });
});