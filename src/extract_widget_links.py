"""Extract brand_id and widget link pairs from Google Sheets."""

from loguru import logger

from config.google_sheets import (
    COLUMN_BRAND_ID,
    COLUMN_SAB_TOP_TOURNAMENT_WIDGET_LINK,
    GOOGLE_SHEET_SAB_WIDGET_MANAGEMENT_ID,
    GOOGLE_SHEET_SAB_WIDGET_MANAGEMENT_WIDGET_LINKS_SHEET_NAME,
)
from lib.google_sheets import read_sheet


def extract_widget_links() -> list[dict[str, str]]:
    """Read widget links sheet and return list of {brand_id, widget_link} dicts."""
    rows = read_sheet(
        GOOGLE_SHEET_SAB_WIDGET_MANAGEMENT_ID,
        GOOGLE_SHEET_SAB_WIDGET_MANAGEMENT_WIDGET_LINKS_SHEET_NAME,
    )

    if not rows:
        logger.warning("Sheet is empty")
        return []

    def _parse_rows() -> list[dict[str, str]]:
        """Find target columns by header name and extract values."""
        headers = rows[0]
        brand_idx = headers.index(COLUMN_BRAND_ID)
        link_idx = headers.index(COLUMN_SAB_TOP_TOURNAMENT_WIDGET_LINK)

        results = []
        for row in rows[1:]:
            if len(row) > max(brand_idx, link_idx):
                results.append({
                    COLUMN_BRAND_ID: row[brand_idx],
                    COLUMN_SAB_TOP_TOURNAMENT_WIDGET_LINK: row[link_idx],
                })
        return results

    data = _parse_rows()
    logger.info("Extracted {count} widget links", count=len(data))
    return data
