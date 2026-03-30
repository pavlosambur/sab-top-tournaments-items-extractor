"""Login to backoffice instances via Selenium."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from loguru import logger

from config.selenium import (
    FORM_ERROR_XPATH,
    LOGGED_IN_INDICATOR_XPATH,
    LOGIN_INPUT_XPATH,
    LOGIN_SUBMIT_XPATH,
    PASSWORD_INPUT_XPATH,
    SELENIUM_WAIT_TIMEOUT,
    TWO_FA_INPUT_XPATH,
    TWO_FA_SUBMIT_XPATH,
)
from config.settings import credentials
from lib.actions import click_and_wait, fill_and_verify, wait_for_element


def login_to_all(browser: WebDriver, base_urls: list[str]) -> None:
    """Login to each base URL sequentially."""
    for url in base_urls:
        _login(browser, url)
    logger.info("Logged in to {count} instances", count=len(base_urls))


def _login(browser: WebDriver, base_url: str) -> None:
    """Login to a single backoffice instance."""
    logger.info("Logging in to {url}", url=base_url)
    browser.get(base_url)

    def _fill_credentials() -> None:
        """Fill login and password fields."""
        fill_and_verify(browser, LOGIN_INPUT_XPATH, credentials.ubo_login)
        fill_and_verify(browser, PASSWORD_INPUT_XPATH, credentials.ubo_password)

    def _submit_login() -> None:
        """Submit login form and wait for 2FA page."""
        click_and_wait(browser, LOGIN_SUBMIT_XPATH, TWO_FA_INPUT_XPATH)

    def _handle_two_fa() -> None:
        """Read 2FA code from terminal, fill and submit. Retry on wrong code."""
        while True:
            code = input("Введіть код 2FA: ")
            fill_and_verify(browser, TWO_FA_INPUT_XPATH, code)

            element = WebDriverWait(browser, SELENIUM_WAIT_TIMEOUT).until(
                EC.element_to_be_clickable((By.XPATH, TWO_FA_SUBMIT_XPATH))
            )
            element.click()

            WebDriverWait(browser, SELENIUM_WAIT_TIMEOUT).until(
                lambda d: _is_logged_in() or _is_otp_cleared() or _has_form_error()
            )

            if _is_logged_in():
                logger.info("2FA passed")
                return

            logger.warning("Wrong 2FA code, try again")

    def _is_logged_in() -> bool:
        """Check if logged-in indicator is present."""
        return len(browser.find_elements(By.XPATH, LOGGED_IN_INDICATOR_XPATH)) > 0

    def _is_otp_cleared() -> bool:
        """Check if OTP input was cleared (wrong code submitted)."""
        elements = browser.find_elements(By.XPATH, TWO_FA_INPUT_XPATH)
        return len(elements) > 0 and elements[0].get_attribute("value") == ""

    def _has_form_error() -> bool:
        """Check if form validation error appeared."""
        return len(browser.find_elements(By.XPATH, FORM_ERROR_XPATH)) > 0

    def _verify_logged_in() -> None:
        """Verify that login was successful."""
        wait_for_element(browser, LOGGED_IN_INDICATOR_XPATH)
        logger.info("Successfully logged in to {url}", url=base_url)

    _fill_credentials()
    _submit_login()
    _handle_two_fa()
    _verify_logged_in()
