import argparse
from pathlib import Path

from .epub import build_epub
from .feed import fetch_feed


def main():
    parser = argparse.ArgumentParser(description="Convert an RSS feed to an EPUB")
    parser.add_argument("url", help="RSS feed URL")
    parser.add_argument("-o", "--output", required=True, type=Path, help="Output EPUB path")
    args = parser.parse_args()

    print(f"Fetching {args.url}...")
    title, articles = fetch_feed(args.url)
    print(f"Found {len(articles)} articles in '{title}'")

    build_epub(title, articles, args.output)
    print(f"Wrote {args.output}")
