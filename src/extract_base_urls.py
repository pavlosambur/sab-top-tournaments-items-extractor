"""Extract unique base URLs from widget links."""

from urllib.parse import urlparse

from loguru import logger

from config.google_sheets import COLUMN_SAB_TOP_TOURNAMENT_WIDGET_LINK


def extract_base_urls(widget_links: list[dict[str, str]]) -> list[str]:
    """Extract unique base URLs (scheme + host) from widget link dicts."""
    def _parse_base_url(url: str) -> str:
        """Return scheme://host from a full URL."""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    base_urls = {
        _parse_base_url(row[COLUMN_SAB_TOP_TOURNAMENT_WIDGET_LINK])
        for row in widget_links
        if row.get(COLUMN_SAB_TOP_TOURNAMENT_WIDGET_LINK)
    }

    result = sorted(base_urls)
    logger.info("Extracted {count} unique base URLs", count=len(result))
    return result
