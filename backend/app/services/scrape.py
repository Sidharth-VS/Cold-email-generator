from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

ALLOWED_SCHEMES = {"http", "https"}


def is_safe_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ALLOWED_SCHEMES and bool(parsed.netloc)
    except Exception:
        return False


def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&\w+;', ' ', text)
    text = re.sub(r'[\n\r\t]', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()


def get_webpage_text(url):
    if not is_safe_url(url):
        raise ValueError("Invalid or unsafe URL")
    loader = WebBaseLoader(url)
    docs = loader.load()
    if not docs:
        raise ValueError("No content fetched from URL")
    page_data = docs.pop().page_content
    content = clean_text(page_data)
    return content