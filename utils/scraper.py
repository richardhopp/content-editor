# utils/scraper.py
import requests
from bs4 import BeautifulSoup
import re

def fetch_page(url: str, timeout: int = 10) -> BeautifulSoup:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AI-WP-Content-Manager/1.0; +https://yourdomain.com/)"
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def extract_images(soup: BeautifulSoup) -> list:
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src:
            images.append(src)
    return images

def extract_text(soup: BeautifulSoup) -> str:
    paragraphs = soup.find_all("p")
    if paragraphs:
        return "\n".join([p.get_text() for p in paragraphs])
    else:
        return soup.get_text(separator="\n")

def extract_meta(soup: BeautifulSoup) -> dict:
    meta_data = {}
    for meta in soup.find_all("meta"):
        name = meta.get("name", "").lower()
        if name in ["description", "keywords"]:
            meta_data[name] = meta.get("content", "")
    return meta_data

def extract_youtube_video(soup: BeautifulSoup) -> str:
    iframe = soup.find("iframe", src=re.compile("youtube.com/embed/"))
    if iframe:
        return iframe.get("src")
    return ""

def scrape_website(url: str) -> dict:
    try:
        soup = fetch_page(url)
        return {
            "text": extract_text(soup),
            "images": extract_images(soup),
            "meta": extract_meta(soup),
            "youtube": extract_youtube_video(soup)
        }
    except Exception as e:
        return {"error": str(e)}
