"""
UberScrape - AI-powered web scraping that returns structured data
"""

__version__ = "0.1.0"
__author__ = "Doug Simpson"

from .core.scraper import WebScraper
from .core.extractor import extract_structured_data
from .utils.schema import load_schema

__all__ = ["WebScraper", "extract_structured_data", "load_schema"]
