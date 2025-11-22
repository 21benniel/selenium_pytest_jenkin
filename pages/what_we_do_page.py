from base.base_page import BasePage
import utilities.custom_logger as cl
import logging
import allure

class WhatWeDoPage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _cloud_operating_model_header_xpath = "//h2[contains(text(), 'Nutanix Delivers the Ideal Platform for Your Business')]"
    
    # Dynamic locator for items
    def _getItemLocator(self, itemText):
        return f"//h3[contains(text(), \"{itemText}\")]"

    @allure.step("Wait for 'Cloud Operating Model' section to appear")
    def waitForCloudOperatingModelSection(self):
        self.waitForElementPresence(self._cloud_operating_model_header_xpath, locatorType="xpath")

    @allure.step("Verify Cloud Operating Model items: {itemsList}")
    def verifyCloudOperatingModelItems(self, itemsList):
        missing_items = []
        for item in itemsList:
            with allure.step(f"Checking for item: {item}"):
                locator = self._getItemLocator(item)
                isPresent = self.isElementPresent(locator, locatorType="xpath")
                if not isPresent:
                    missing_items.append(item)
                    self.log.error(f"Item missing: {item}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Missing_Item_{item}", attachment_type=allure.attachment_type.PNG)
                else:
                    self.log.info(f"Item found: {item}")
        
        return missing_items
