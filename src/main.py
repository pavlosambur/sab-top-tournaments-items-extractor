"""Main orchestrator for the extractor pipeline."""

from lib.logger import setup_logger
from loguru import logger


def run() -> None:
    """Run the extractor pipeline."""
    setup_logger()
    logger.info("Pipeline started")

    from src.extract_widget_links import extract_widget_links
    widget_links = extract_widget_links()

    from src.extract_base_urls import extract_base_urls
    base_urls = extract_base_urls(widget_links)

    from lib.browser import create_browser
    browser = create_browser()

    from src.login import login_to_all
    login_to_all(browser, base_urls)

    from src.process_widgets import collect_item_links
    item_links = collect_item_links(browser, widget_links)

    from src.process_items import process_items
    items_data = process_items(browser, item_links)

    browser.quit()
    logger.info("Browser closed")

    from config.google_sheets import (
        GOOGLE_SHEET_SAB_WIDGET_MANAGEMENT_ID,
        SHEET_TMP_ITEMS_DATA,
    )
    from lib.google_sheets import append_to_sheet
    append_to_sheet(
        GOOGLE_SHEET_SAB_WIDGET_MANAGEMENT_ID,
        SHEET_TMP_ITEMS_DATA,
        items_data,
    )

    logger.info("Pipeline finished")


if __name__ == "__main__":
    run()
