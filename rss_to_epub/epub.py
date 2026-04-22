import subprocess
import tempfile
from pathlib import Path

from .feed import Article


def build_epub(title: str, articles: list[Article], output: Path) -> None:
    """Build an EPUB from articles using Pandoc."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        chapter_files = []

        for i, article in enumerate(articles):
            chapter_path = tmp / f"{i:04d}.html"
            html = f"<h1>{article.title}</h1>\n{article.html}"
            chapter_path.write_text(html, encoding="utf-8")
            chapter_files.append(str(chapter_path))

        output.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "pandoc",
            "--to=epub",
            f"--metadata=title:{title}",
            "--toc",
            "--split-level=1",
            "-o",
            str(output),
            *chapter_files,
        ]
        subprocess.run(cmd, check=True)
