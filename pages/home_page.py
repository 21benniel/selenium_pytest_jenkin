from base.base_page import BasePage
import utilities.custom_logger as cl
import logging
import allure
import time

class HomePage(BasePage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # Locators
    _what_we_do_link = "What We Do" # Link Text
    _solutions_menu_button = "//button[@aria-label='Open Solutions menu']" # XPath
    _database_as_service_link = "//a[contains(@href, '/products/database-service')]" # XPath
    
    @allure.step("Click on 'What We Do' link")
    def clickWhatWeDo(self):
        self.elementClick(self._what_we_do_link, locatorType="link")
        
    @allure.step("Navigate to Nutanix Home Page")
    def navigateToHome(self):
        self.driver.get("https://www.nutanix.com/")

    @allure.step("Navigate to Database as Service Page")
    def navigateToDatabaseAsService(self):
        # Direct navigation to avoid menu interaction issues
        self.log.info("Navigating directly to Database as Service page")
        self.driver.get("https://www.nutanix.com/products/database-service")
