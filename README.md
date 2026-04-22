# rss-to-epub

Convert an RSS feed into an EPUB, with each article as a chapter.

## Usage

```
rss-to-epub https://example.com/feed -o output.epub
```

Requires `pandoc` to be available on your PATH.

## Development

Enter the dev shell (provides Python, uv, and pandoc):

```
nix develop
```

Install dependencies:

```
uv sync
```
