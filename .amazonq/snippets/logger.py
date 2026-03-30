"""Configure loguru to output VS Code-clickable file paths."""

import os
import sys

import loguru
from loguru import logger

LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[rel_path]}:{line}</cyan> | "
    "<level>{message}</level>"
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _enrich_record(record: "loguru.Record") -> bool:
    """Add relative file path to record and allow the message through."""
    abs_path = record["file"].path
    try:
        record["extra"]["rel_path"] = os.path.relpath(abs_path, PROJECT_ROOT)
    except ValueError:
        record["extra"]["rel_path"] = abs_path
    return True


def setup_logger() -> None:
    """Replace default loguru handler with VS Code-friendly format."""
    logger.remove()
    logger.add(sys.stderr, format=LOG_FORMAT, filter=_enrich_record)
