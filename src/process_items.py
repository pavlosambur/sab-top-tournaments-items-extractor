"""Open item pages and extract data."""

import re

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from loguru import logger

from config.google_sheets import COLUMN_ITEM_URL
from config.selenium import (
    ITEM_NAME_XPATH,
    ITEM_PAGE_LOADED_XPATH,
    ITEM_STATUS_XPATH,
    ITEM_WEB_LINK_XPATH,
)
from lib.actions import wait_for_element

BRAND_ID_PATTERN = re.compile(r"/brands/([^/]+)/cms-mfe/")


def process_items(browser: WebDriver, item_links: list[str]) -> list[dict[str, str]]:
    """Open each item link, collect data from each page."""
    results: list[dict[str, str]] = []

    for url in item_links:
        data = _extract_item_data(browser, url)
        results.append(data)

    logger.info("Processed {count} items", count=len(results))
    return results


def _extract_item_data(browser: WebDriver, url: str) -> dict[str, str]:
    """Navigate to item page and extract item_name, web_link, status."""
    logger.info("Opening item: {url}", url=url)
    browser.get(url)
    wait_for_element(browser, ITEM_PAGE_LOADED_XPATH)
    wait_for_element(browser, ITEM_NAME_XPATH)
    wait_for_element(browser, ITEM_WEB_LINK_XPATH)
    wait_for_element(browser, ITEM_STATUS_XPATH)

    item_name = browser.find_element(By.XPATH, ITEM_NAME_XPATH).get_attribute("value")
    web_link = browser.find_element(By.XPATH, ITEM_WEB_LINK_XPATH).text
    status = browser.execute_script(
        "return Array.from(arguments[0].childNodes)"
        ".filter(n => n.nodeType === Node.TEXT_NODE)"
        ".map(n => n.textContent.trim().toLowerCase())"
        ".find(t => t) || ''",
        browser.find_element(By.XPATH, ITEM_STATUS_XPATH),
    )

    brand_id = _extract_brand_id(url)

    if not item_name or not web_link or not status:
        raise RuntimeError(f"Missing required fields on {url}: item_name={item_name}, web_link={web_link}, status={status}")

    logger.info("Extracted item: {name}, brand: {brand}, status: {status}", name=item_name, brand=brand_id, status=status)
    return {"brand_id": brand_id, "item_name": item_name, "web_link": web_link, "status": status, COLUMN_ITEM_URL: url}


def _extract_brand_id(url: str) -> str:
    """Extract brand_id from item URL."""
    match = BRAND_ID_PATTERN.search(url)
    if not match:
        raise RuntimeError(f"Cannot extract brand_id from URL: {url}")
    return match.group(1)
