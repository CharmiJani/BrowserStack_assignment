from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.options import ArgOptions
import threading
import os
from main import run_scraper

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

BROWSERSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"


def run_test(capabilities):
    browser = capabilities.get("browserName", "").lower()

    if browser == "firefox":
        options = FirefoxOptions()
        
    elif browser == "chrome":
        options = ChromeOptions()
    else:
        options = ArgOptions() 

    for key, value in capabilities.items():
        options.set_capability(key, value)

    driver = webdriver.Remote(
        command_executor=BROWSERSTACK_URL,
        options=options
    )

    print("Running on:", capabilities.get("browserName", capabilities.get("deviceName")))

    run_scraper(driver)

    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed","reason": "Scraper executed successfully"}}'
    )

    driver.quit()


browsers = [

{
    "browserName": "Chrome",
    "browserVersion": "latest",
    "bstack:options": {
        "os": "Windows",
        "osVersion": "11"
    }
},

{
    "browserName": "Firefox",
    "browserVersion": "latest",
    "bstack:options": {
        "os": "Windows",
        "osVersion": "10"
    }
},

{
    "browserName": "Safari",
    "browserVersion": "latest",
    "bstack:options": {
        "os": "OS X",
        "osVersion": "Monterey"
    }
},

{
    "browserName": "Chrome",
    "bstack:options": {
        "deviceName": "Samsung Galaxy S22",
        "osVersion": "12.0",
        "realMobile": "true"
    }
},

{
    "browserName": "Safari",
    "bstack:options": {
        "deviceName": "iPhone 13",
        "osVersion": "15",
        "realMobile": "true"
    }
}

]

threads = []

for caps in browsers:
    t = threading.Thread(target=run_test, args=(caps,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()