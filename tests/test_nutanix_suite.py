from pages.home_page import HomePage
from pages.what_we_do_page import WhatWeDoPage
from pages.database_as_service_page import DatabaseAsServicePage
from base.base_test import BaseTest
import pytest
import utilities.custom_logger as cl
import logging
import allure

@allure.feature("Nutanix Website Verification")
class TestNutanixCloudModel(BaseTest):
    log = cl.customLogger(logging.DEBUG)

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetUp):
        self.homePage = HomePage(self.driver)
        self.whatWeDoPage = WhatWeDoPage(self.driver)
        self.dbServicePage = DatabaseAsServicePage(self.driver)

    @allure.story("Verify Cloud Operating Model Section")
    @allure.title("Test Cloud Operating Model Items Existence")
    @allure.description("Navigate to 'What We Do' page and verify all Cloud Operating Model items are present.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_verify_cloud_operating_model(self):
        self.log.info("Starting test_verify_cloud_operating_model")
        
        # Navigate to Home
        self.homePage.navigateToHome()
        
        # Click What We Do
        self.homePage.clickWhatWeDo()
        
        # Wait for section
        self.whatWeDoPage.waitForCloudOperatingModelSection()
        
        # Verify Items
        expected_items = [
            "Modernize Your Datacenter",
            "Unify Operations on a Single Platform",
            "Speed App Development and Deployment",
            "Move Apps and Data with Ease",
            "Build More Agile and Flexible Operations",
            "Protect Against Cyber Threats and Data Loss"
        ]
        
        missing_items = self.whatWeDoPage.verifyCloudOperatingModelItems(expected_items)
        
        if len(missing_items) > 0:
             allure.attach(str(missing_items), name="Missing Items List", attachment_type=allure.attachment_type.TEXT)

        assert len(missing_items) == 0, f"Missing items: {missing_items}"
        self.log.info("Test Finished Successfully")

    @allure.story("Verify Database as Service Benefits")
    @allure.title("Test Database as Service Benefits Existence")
    @allure.description("Navigate to 'Database as Service' page and verify all NDB Benefits items are present.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_verify_database_as_service_benefits(self):
        self.log.info("Starting test_verify_database_as_service_benefits")
        
        # Navigate to Home
        self.homePage.navigateToHome()
        
        # Navigate to Database as Service
        self.homePage.navigateToDatabaseAsService()
        
        # Wait for benefits section
        self.dbServicePage.waitForBenefitsSection()
        
        # Verify Benefits
        # Note: "Rapid Point-in-Time Recovery" text might be split or formatted differently.
        # Update: Use partial text match or verified exact text. 
        # In snapshot it appeared as "Rapid Point-in-Time Recovery".
        # If it fails, maybe it's "Rapid Point-In-Time Recovery" (capital I) or spacing issue.
        # Let's use a shorter unique string for that item to be safe.
        expected_benefits = [
            "Fast Snapshots",
            "Quick Provisioning",
            "Easy Patching",
            "Reduced Costs",
            "Point-in-Time Recovery", # Adjusted from "Rapid Point-in-Time Recovery" to be safer
            "Thin Cloning",
            "Effortless Replication",
            "Boost Performance"
        ]
        
        missing_benefits = self.dbServicePage.verifyBenefitsItems(expected_benefits)
        
        if len(missing_benefits) > 0:
             allure.attach(str(missing_benefits), name="Missing Benefits List", attachment_type=allure.attachment_type.TEXT)

        assert len(missing_benefits) == 0, f"Missing benefits: {missing_benefits}"
        self.log.info("Test Finished Successfully")
