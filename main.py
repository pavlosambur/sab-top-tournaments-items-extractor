"""Entry point for sab-top-tournaments-items-extractor."""

from lib.logger import setup_logger
from src.main import run


def main() -> None:
    """Entry point: setup and launch pipeline."""
    setup_logger()
    run()


if __name__ == "__main__":
    main()
