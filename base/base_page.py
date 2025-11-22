from base.selenium_driver import SeleniumDriver

class BasePage(SeleniumDriver):
    """
    Base Page class that inherits from SeleniumDriver
    """
    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def verifyPageTitle(self, titleToVerify):
        try:
            actualTitle = self.driver.title
            return actualTitle == titleToVerify
        except:
            self.log.error("Failed to get page title")
            return False

