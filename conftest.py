import json
import os
import urllib
import subprocess
import pytest
from playwright.sync_api import sync_playwright
# from dotenv import load_dotenv

# load_dotenv("../.env", override=True)

capabilities = {
    "browserName": "Chrome",  # Browsers allowed: `Chrome`, `MicrosoftEdge`, `pw-chromium`, `pw-firefox` and `pw-webkit`
    "browserVersion": "latest",
    "LT:Options": {
        "platform": "Windows 11",
        "build": "Integration Test Build",
        "name": "Python Integration Test (Pytest)",
        "user": os.getenv("LT_USERNAME"),
        "accessKey": os.getenv("LT_ACCESS_KEY"),
        "network": True,
        "video": True,
        "console": True,
        "headless": True,
        "tunnel": False,  # Add tunnel configuration if testing locally hosted webpage
        "tunnelName": "",  # Optional
        "geoLocation": "",  # country code can be fetched from https://www.lambdatest.com/capabilities-generator/
    },
}


# Pytest browser fixture (for cloud testing)
@pytest.fixture(name="browser", scope="module")
def browser():
    with sync_playwright() as playwright:
        playwrightVersion = (
            str(subprocess.getoutput("playwright --version")).strip().split(" ")[1]
        )
        capabilities["LT:Options"]["playwrightClientVersion"] = playwrightVersion
        lt_cdp_url = (
            "wss://cdp.lambdatest.com/playwright?capabilities="
            + urllib.parse.quote(json.dumps(capabilities))
        )
        browser = playwright.chromium.connect(lt_cdp_url, timeout=30000)
        yield browser
        browser.close()


# Pytest page fixture (for cloud testing)
@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()


# sets status of test case if passed or failed
@pytest.fixture
def set_test_status(page):
    def _set_test_status(status, remark):
        page.evaluate(
            "_ => {}",
            'lambdatest_action: {"action": "setTestStatus", "arguments": {"status":"'
            + status
            + '", "remark": "'
            + remark
            + '"}}',
        )

    yield _set_test_status