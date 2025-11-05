import pytest
from playwright.sync_api import sync_playwright
from typing import Literal
from time import sleep
from playwright.sync_api._generated import BrowserContext, Page
import logging
import allure
from conftest import base_url1, base_url2, base_url3
from tests.Web.login import log_in
from addBal import add_balance
from onewayflight import search_oneway
from travellerDetails import flight_summary
from ssr import flight_ssr
from jsonData import select_date
from issueOrder import issue_order

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

def capture_and_log_action(action: str):
    logger.info(f"Action: {action}")
    allure.attach(action, name="Action Log", attachment_type=allure.attachment_type.TEXT)

# @pytest.mark.login
# @allure.feature("Landing page button")
# @allure.story("User should go to the landing page and check all buttons")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_b2bstaging_login(base_url1: Literal['https://bdf.centralindia.cloudapp.azure.com/'], setup_browser: tuple[Page, BrowserContext]):
#     page, context = setup_browser

#     capture_and_log_action(f"Navigating to: {base_url1}")
#     page.goto(base_url1, timeout=60000)
#     page.wait_for_load_state('domcontentloaded')

#     capture_and_log_action(f"Current URL after navigation: {page.url}")
    
#     try:
#         capture_and_log_action("Go to the B2B landing page")
#         log_in(page, context)
#         page.wait_for_load_state('load')
#     except Exception as e:
#         capture_and_log_action(f"Error occurred: {str(e)}")
#         if not page.is_closed():
#             page.screenshot(path="screenshot_failure.png")
#             with open("screenshot_failure.png", "rb") as f:
#                 pytest.fail(f"Test failed with error: {str(e)}")


# @pytest.mark.addBalance
# @allure.feature("Deposite section")
# @allure.story("User should go to the deposite section to add balance")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_b2bstaging_balance(base_url1: Literal['https://bdf.centralindia.cloudapp.azure.com/'], setup_browser: tuple[Page, BrowserContext]):
#     page, context = setup_browser

#     capture_and_log_action(f"Navigating to: {base_url1}")
#     page.goto(base_url1, timeout=60000)
#     page.wait_for_load_state('domcontentloaded')

#     capture_and_log_action(f"Current URL after navigation: {page.url}")
    
#     try:
#         capture_and_log_action("Go to the B2B landing page")
#         add_balance(page)
#         page.wait_for_load_state('load')
#     except Exception as e:
#         capture_and_log_action(f"Error occurred: {str(e)}")
#         if not page.is_closed():
#             page.screenshot(path="screenshot_failure.png")
#             with open("screenshot_failure.png", "rb") as f:
#                 pytest.fail(f"Test failed with error: {str(e)}")


# @pytest.mark.loginLive
# @allure.feature("Landing page button")
# @allure.story("User should go to the landing page and check all buttons")
# @allure.severity(allure.severity_level.CRITICAL)
# def test_b2b(base_url3: Literal['https://bdfare.com/'], setup_browser: tuple[Page, BrowserContext]):
#     page, context = setup_browser

#     capture_and_log_action(f"Navigating to: {base_url3}")
#     page.goto(base_url3, timeout=60000)
#     page.wait_for_load_state('domcontentloaded')

#     capture_and_log_action(f"Current URL after navigation: {page.url}")
    
#     try:
#         capture_and_log_action("Go to the B2B landing page")
#         log_in(page, context)
#         page.wait_for_load_state('load')
#     except Exception as e:
#         capture_and_log_action(f"Error occurred: {str(e)}")
#         if not page.is_closed():
#             page.screenshot(path="screenshot_failure.png")
#             with open("screenshot_failure.png", "rb") as f:
#                 allure.attach(f.read(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
#             pytest.fail(f"Test failed with error: {str(e)}")

    
@pytest.mark.oneway
@allure.feature("Flight section")
@allure.story("User should go to search a flight for oneway")
@allure.severity(allure.severity_level.CRITICAL)
def test_b2bstaging_searchFlight(base_url1: Literal['https://bdf.centralindia.cloudapp.azure.com/'], setup_browser: tuple[Page, BrowserContext]):
    page, context = setup_browser
    capture_and_log_action(f"Navigating to: {base_url1}")
    page.goto(base_url1, timeout=60000)
    page.wait_for_load_state('domcontentloaded')
    capture_and_log_action(f"Current URL after navigation: {page.url}")
    try:
        capture_and_log_action("Go to the B2B landing page")
        search_oneway(page, select_date)
        page.wait_for_load_state('load')
        flight_summary(page)
        page.wait_for_load_state('load')
        flight_ssr(page)
        page.wait_for_load_state('load')
        issue_order(page)

    except Exception as e:
        capture_and_log_action(f"Error occurred: {str(e)}")
        if not page.is_closed():
            page.screenshot(path="screenshot_failure.png")
            with open("screenshot_failure.png", "rb") as f:
                pytest.fail(f"Test failed with error: {str(e)}")


@pytest.mark.flight
@allure.feature("Landing page button")
@allure.story("User should go to the landing page and check all buttons")
@allure.severity(allure.severity_level.CRITICAL)
def test_flight(base_url1: Literal['https://bdf.centralindia.cloudapp.azure.com/'], setup_browser: tuple[Page, BrowserContext]):
    page, context = setup_browser

    capture_and_log_action(f"Navigating to: {base_url1}")
    page.goto(base_url1, timeout=60000)
    page.wait_for_load_state('domcontentloaded')
    capture_and_log_action(f"Current URL after navigation: {page.url}")
    try:
        capture_and_log_action("Go to the B2B landing page")
        log_in(page, context)
        page.wait_for_load_state('load')
        # add_balance(page)
        # page.wait_for_load_state('load')
        search_oneway(page, select_date)
        page.wait_for_load_state('load')
        flight_summary(page)
        page.wait_for_load_state('load')
        flight_ssr(page)
        page.wait_for_load_state('load')
        issue_order(page)

    except Exception as e:
        capture_and_log_action(f"Error occurred: {str(e)}")
        if not page.is_closed():
            page.screenshot(path="screenshot_failure.png")
            with open("screenshot_failure.png", "rb") as f:
                allure.attach(f.read(), name="Failure Screenshot", attachment_type=allure.attachment_type.PNG)
            pytest.fail(f"Test failed with error: {str(e)}")