"""Browser lifecycle management."""

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from loguru import logger


def create_browser() -> webdriver.Firefox:
    """Create and return a Firefox browser instance."""
    options = Options()
    browser = webdriver.Firefox(options=options)
    logger.info("Browser created")
    return browser
