"""Selenium action helpers with retries and state verification."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from loguru import logger

from config.selenium import SELENIUM_RETRIES, SELENIUM_WAIT_TIMEOUT


def fill_and_verify(browser: WebDriver, xpath: str, value: str) -> None:
    """Fill an input field and verify the value was set."""
    for attempt in range(1, SELENIUM_RETRIES + 1):
        element = WebDriverWait(browser, SELENIUM_WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.clear()
        element.send_keys(value)

        if element.get_attribute("value") == value:
            logger.debug("Filled field: {xpath}", xpath=xpath)
            return

        logger.warning("Fill attempt {attempt} failed for {xpath}", attempt=attempt, xpath=xpath)

    raise RuntimeError(f"Failed to fill field after {SELENIUM_RETRIES} retries: {xpath}")


def click_and_wait(browser: WebDriver, xpath: str, wait_xpath: str) -> None:
    """Click an element and wait for another element to appear."""
    for attempt in range(1, SELENIUM_RETRIES + 1):
        element = WebDriverWait(browser, SELENIUM_WAIT_TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        element.click()

        try:
            WebDriverWait(browser, SELENIUM_WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, wait_xpath))
            )
            logger.debug("Clicked {xpath}, verified {wait_xpath}", xpath=xpath, wait_xpath=wait_xpath)
            return
        except Exception:
            logger.warning("Click attempt {attempt} failed for {xpath}", attempt=attempt, xpath=xpath)

    raise RuntimeError(f"Failed to click and verify after {SELENIUM_RETRIES} retries: {xpath}")


def wait_for_element(browser: WebDriver, xpath: str) -> None:
    """Wait for an element to be present on the page."""
    WebDriverWait(browser, SELENIUM_WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    logger.debug("Element found: {xpath}", xpath=xpath)
