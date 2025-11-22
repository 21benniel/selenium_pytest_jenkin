import pytest
from selenium import webdriver
import allure
from datetime import datetime
import os

@pytest.fixture(scope="class")
def oneTimeSetUp(request):
    print("Running one time setUp")
    options = webdriver.ChromeOptions()
    
    # Running in Jenkins/CI typically requires headless mode and other specific flags
    # You can check for an env var or just enable these by default for stability
    options.add_argument('--headless') 
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(options=options)
    
    if request.cls is not None:
        request.cls.driver = driver
        
    yield driver
    driver.quit()
    print("Running one time tearDown")

@pytest.fixture()
def setUp():
    print("Running method level setUp")
    yield
    print("Running method level tearDown")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to capture screenshot on failure and attach to Allure report
    """
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == 'call' and rep.failed:
        driver = None
        if "oneTimeSetUp" in item.funcargs:
             driver = item.funcargs["oneTimeSetUp"]
        elif "classSetup" in item.funcargs:
             # Sometimes class setup might not directly expose driver but the instance does
             if item.instance:
                 driver = getattr(item.instance, 'driver', None)
        
        # If we couldn't find driver in args, try to look at the class instance
        if not driver and item.instance:
             driver = getattr(item.instance, 'driver', None)
             
        if driver:
            now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"screenshot_{item.name}_{now}.png"
            try:
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=file_name,
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Failed to capture screenshot: {e}")
