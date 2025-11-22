from base.base_page import BasePage
import utilities.custom_logger as cl
import logging
import allure

class DatabaseAsServicePage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _benefits_header_xpath = "//h2[contains(text(), 'NDB Benefits')]"
    
    # Dynamic locator for benefits items
    # Update locator to be less specific about tag type or hierarchy
    def _getBenefitLocator(self, benefitText):
        # Search for any element containing the text, likely headers
        # Using translate for case-insensitive matching if needed, but sticking to exact first
        return f"//*[contains(text(), \"{benefitText}\")]"

    @allure.step("Wait for 'NDB Benefits' section to appear")
    def waitForBenefitsSection(self):
        self.waitForElementPresence(self._benefits_header_xpath, locatorType="xpath")
        try:
            element = self.getElement(self._benefits_header_xpath, locatorType="xpath")
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        except:
            pass

    @allure.step("Verify NDB Benefits items: {benefitsList}")
    def verifyBenefitsItems(self, benefitsList):
        missing_items = []
        for item in benefitsList:
            with allure.step(f"Checking for benefit: {item}"):
                locator = self._getBenefitLocator(item)
                
                # Try to find element
                isPresent = self.isElementPresent(locator, locatorType="xpath")
                
                if not isPresent:
                    # Try one more time with a wait
                    element = self.waitForElementPresence(locator, locatorType="xpath", timeout=5)
                    if element:
                        isPresent = True
                
                if not isPresent:
                    missing_items.append(item)
                    self.log.error(f"Benefit missing: {item}")
                    allure.attach(self.driver.get_screenshot_as_png(), name=f"Missing_Benefit_{item}", attachment_type=allure.attachment_type.PNG)
                else:
                    self.log.info(f"Benefit found: {item}")
        
        return missing_items
