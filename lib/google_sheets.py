"""Google Sheets API client wrapper."""

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from loguru import logger

from config.settings import settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def _build_service():
    """Create and return Google Sheets API service."""
    creds = Credentials.from_service_account_file(
        settings.google_service_account_path, scopes=SCOPES
    )
    return build("sheets", "v4", credentials=creds)


def read_sheet(spreadsheet_id: str, sheet_name: str) -> list[list[str]]:
    """Read all rows from a sheet and return as list of rows (first row = headers)."""
    service = _build_service()
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=sheet_name)
        .execute()
    )
    rows = result.get("values", [])
    logger.info("Read sheet '{sheet}': {count} rows", sheet=sheet_name, count=len(rows))
    return rows


def append_to_sheet(spreadsheet_id: str, sheet_name: str, rows: list[dict[str, str]]) -> None:
    """Append rows to the end of a sheet, mapping values to existing header columns."""
    service = _build_service()

    all_data = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=sheet_name)
        .execute()
    )
    existing_rows = all_data.get("values", [])
    headers = existing_rows[0] if existing_rows else []

    start_col = chr(ord("A") + _find_header_col_offset(service, spreadsheet_id, sheet_name))
    start_row = len(existing_rows) + 1
    data = [[row.get(h, "") for h in headers] for row in rows]

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!{start_col}{start_row}",
        valueInputOption="RAW",
        body={"values": data},
    ).execute()

    logger.info("Appended {count} rows to '{sheet}'", count=len(rows), sheet=sheet_name)


def _find_header_col_offset(service, spreadsheet_id: str, sheet_name: str) -> int:
    """Find the column offset where headers start."""
    first_row = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!1:1")
        .execute()
    )
    cells = first_row.get("values", [[]])[0]
    for i, cell in enumerate(cells):
        if cell.strip():
            return i
    return 0
