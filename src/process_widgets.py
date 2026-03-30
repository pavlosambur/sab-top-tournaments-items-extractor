"""Open widget links and collect item URLs from widget pages."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger

from config.google_sheets import COLUMN_SAB_TOP_TOURNAMENT_WIDGET_LINK
from config.selenium import WIDGET_ITEM_LINK_XPATH, WIDGET_PAGE_LOADED_XPATH
from lib.actions import wait_for_element


def collect_item_links(browser: WebDriver, widget_links: list[dict[str, str]]) -> list[str]:
    """Open each widget link, collect all item URLs into a single list."""
    all_items: list[str] = []

    for row in widget_links:
        url = row[COLUMN_SAB_TOP_TOURNAMENT_WIDGET_LINK]
        items = _extract_items_from_page(browser, url)
        all_items.extend(items)

    logger.info("Collected {count} item links total", count=len(all_items))
    return all_items


def _extract_items_from_page(browser: WebDriver, url: str) -> list[str]:
    """Navigate to widget page and extract item links."""
    logger.info("Opening widget: {url}", url=url)
    browser.get(url)
    wait_for_element(browser, WIDGET_PAGE_LOADED_XPATH)

    elements = browser.find_elements(By.XPATH, WIDGET_ITEM_LINK_XPATH)
    items = [el.get_attribute("href") for el in elements if el.get_attribute("href")]

    logger.info("Found {count} items on {url}", count=len(items), url=url)
    return items
