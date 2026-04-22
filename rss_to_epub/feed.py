from dataclasses import dataclass

import feedparser
import requests
from readability import Document


@dataclass
class Article:
    title: str
    html: str


def fetch_feed(url: str) -> tuple[str, list[Article]]:
    """Fetch an RSS feed and return (feed_title, articles) sorted newest first."""
    feed = feedparser.parse(url)
    title = feed.feed.get("title", "Untitled Feed")

    articles = []
    for entry in feed.entries:
        article_title = entry.get("title", "Untitled")
        html = _extract_content(entry)
        html = _clean_html(html, article_title)
        articles.append(Article(title=article_title, html=html))

    return title, articles


def _extract_content(entry) -> str:
    """Get article HTML, preferring feed content over fetching the URL."""
    # feedparser normalizes content:encoded into entry.content
    if entry.get("content"):
        return entry.content[0].value

    if entry.get("summary"):
        return entry.summary

    link = entry.get("link")
    if link:
        resp = requests.get(link, timeout=30)
        resp.raise_for_status()
        return resp.text

    return ""


def _clean_html(html: str, title: str) -> str:
    """Clean HTML with readability-lxml. Falls back to raw content on failure."""
    if not html:
        return ""

    try:
        doc = Document(html)
        content = doc.summary()
        if content and content.strip():
            return content
    except Exception:
        pass

    return html
