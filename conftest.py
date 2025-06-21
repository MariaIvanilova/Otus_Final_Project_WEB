import pytest
import datetime
from selenium import webdriver
import logging

import pymysql
import pymysql.cursors
from database.bitnami_opencart import (
    delete_product,
    add_product,
    delete_customer_by_email,
)


default_url = "http://192.168.100.9:8085"
default_executor = "192.168.100.9"
log_level = "DEBUG"


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="browser for tests"
    )
    parser.addoption("--bv", action="store", help="browser version")
    parser.addoption(
        "--headless",
        action="store",
        default=None,
        help="enable/disable headless mode: 'true' or 'false'",
    )
    parser.addoption(
        "--remote", action="store_true", help="remote launching by default"
    )
    parser.addoption("--url", action="store", default=default_url)
    parser.addoption("--vnc", action="store_true")
    parser.addoption("--executor", action="store", default=default_executor)
    parser.addoption("--db_host", action="store", default="host.docker.internal")


def docker_option(options):
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")


@pytest.fixture
def browser(request):
    logger = logging.getLogger(request.node.name)
    file_handler = logging.FileHandler(f"logs/{request.node.name}.log")
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)
    logger.info("===> Test started at %s" % datetime.datetime.now())
    logger.info("===> Test name: %s" % request.node.name)

    remote = request.config.getoption("remote")
    browser_name = request.config.getoption("browser")

    headless = request.config.getoption("headless")
    if headless is not None:
        headless = headless.lower() == "true"  # "true" -> True, "false" -> False

    browser_version = request.config.getoption("bv")

    logger.info("===> Browser: %s, version: %s" % (browser_name, browser_version))

    vnc = request.config.getoption("vnc")
    executor = request.config.getoption("executor")
    executor_url = f"http://{executor}:4444/wd/hub"

    driver = None
    options = None

    try:
        if remote:
            if browser_name in ["chrome", "ch"]:
                options = webdriver.ChromeOptions()
                docker_option(options)
            elif browser_name in ["firefox", "ff"]:
                options = webdriver.FirefoxOptions()
                docker_option(options)
            elif browser_name in ["edge", "ed"]:
                options = webdriver.EdgeOptions()
                docker_option(options)

            if options:
                options.set_capability("browserVersion", browser_version)
                options.set_capability("selenoid:options", {"name": request.node.name})
                if vnc:
                    options.set_capability("selenoid:options", {"enableVNC": True})
                driver = webdriver.Remote(
                    command_executor=executor_url, options=options
                )

        else:
            if browser_name in ["chrome", "ch"]:
                options = webdriver.ChromeOptions()
                docker_option(options)
                if headless or headless is None:
                    options.add_argument("--headless=new")
                    options.add_argument("--window-size=1920,1080")
                driver = webdriver.Chrome(options=options)
                driver.maximize_window()

            elif browser_name in ["firefox", "ff"]:
                options = webdriver.FirefoxOptions()
                docker_option(options)
                if headless or headless is None:
                    options.add_argument("--headless")
                    options.add_argument("--window-size=1920,1080")
                driver = webdriver.Firefox(options=options)

            elif browser_name in ["edge", "ed"]:
                options = webdriver.EdgeOptions()
                docker_option(options)
                if headless or headless is None:
                    options.add_argument("--headless=new")
                    options.add_argument("--window-size=1920,1080")
                driver = webdriver.Edge(options=options)

        if driver is None:
            raise ValueError(f"Unsupported browser: {browser_name}")

        driver.maximize_window()
        driver.logger = logger  # Добавляем logger к драйверу

        yield driver

        driver.quit()

    except Exception as e:
        logger.error(f"Failed to initialize browser: {e}")
        raise


@pytest.fixture
def url(request):
    return request.config.getoption("--url")


# @pytest.fixture()
# def db_connection():
#     from database.connection import create_connection
#
#     connection = create_connection()
#     yield connection
#     connection.close()


@pytest.fixture(scope="session")
def db_connection(request):
    db_host = request.config.getoption("db_host")

    connection = pymysql.connect(
        host=db_host,
        port=3306,
        database="bitnami_opencart",
        user="bn_opencart",
        password="",
        cursorclass=pymysql.cursors.DictCursor,
    )
    yield connection

    connection.close()


@pytest.fixture(scope="function")
def product_creation(db_connection):
    yield
    delete_product(db_connection)


@pytest.fixture(scope="function")
def product_deletion(db_connection):
    add_product(db_connection)
    yield


@pytest.fixture(scope="function")
def customer_deletion(db_connection):
    emails_to_delete = []
    yield emails_to_delete
    for email in emails_to_delete:
        delete_customer_by_email(db_connection, email)
