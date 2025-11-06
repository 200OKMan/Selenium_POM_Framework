import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

@pytest.fixture(scope="function")
def browser_configuration(request):
    browser_name = request.config.getoption("browser_name")
    driver = None

    if browser_name == "chrome":
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(options=chrome_options)

    elif browser_name == "firefox":
        driver = webdriver.Firefox()
    else:
        raise ValueError("Unsupported browser")

    request.node.driver = driver

    yield driver

    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when in ("call", "setup"):
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):

            reports_dir = os.path.join(os.path.dirname(__file__), "reports")
            if not os.path.exists(reports_dir):
                os.makedirs(reports_dir)

            file_name = os.path.join(
                reports_dir, report.nodeid.replace("::", "_") + ".png"
            )
            print("Saving screenshot to: " + file_name)

            if hasattr(item, "driver"):
                _capture_screenshot(item.driver, file_name)

            if file_name:
                html = (
                    '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" '
                    'onclick="window.open(this.src)" align="right"/></div>' % file_name
                )
                extra.append(pytest_html.extras.html(html))
        report.extras = extra

def _capture_screenshot(driver, file_name):
    driver.get_screenshot_as_file(file_name)