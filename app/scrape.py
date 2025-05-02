from langchain_community.document_loaders import WebBaseLoader
import re

def clean_text(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&\w+;', ' ', text)
    text = re.sub(r'[\n\r\t]', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def get_webpage_text(url):
    loader = WebBaseLoader(url)
    page_data = loader.load().pop().page_content
    content = clean_text(page_data)
    return content