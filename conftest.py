import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )


@pytest.fixture(scope="function")
def browser_configuration(request):
    browser_name = request.config.getoption("browser_name")
    driver = None

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--incognito")
        options.add_argument("--disable-sync")
        options.add_argument("--disable-popup-blocking")
        driver = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)

    elif browser_name == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")
        options.add_argument("window-size=1920,1080")
        driver = webdriver.Edge(options=options)

    elif browser_name == "safari":
        options = SafariOptions()
        driver = webdriver.Safari(options=options)
        driver.set_window_size(1920, 1080)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    request.node.driver = driver
    yield driver

    if driver is not None:
        driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):

            if hasattr(item, "driver") and item.driver:
                reports_dir = os.path.join(os.path.dirname(__file__), "reports")
                if not os.path.exists(reports_dir):
                    os.makedirs(reports_dir)

                file_name = report.nodeid.replace("::", "_") + ".png"
                file_name = file_name.replace("/", "_").replace("\\", "_")

                destination_file = os.path.join(reports_dir, file_name)

                try:
                    _capture_screenshot(item.driver, destination_file)

                    if destination_file:
                        html = (
                            f'<div><img src="{file_name}" alt="screenshot" '
                            'style="width:304px;height:228px;" '
                            'onclick="window.open(this.src)" align="right"/></div>'
                        )
                        extra.append(pytest_html.extras.html(html))
                except Exception:
                    pass

        report.extras = extra


def _capture_screenshot(driver, file_name):
    driver.get_screenshot_as_file(file_name)