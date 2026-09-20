#!/usr/bin/env python3
"""Pull the manual pages of both git-ftp implementations into docs/reference/.

The manuals live in the tool repositories, written as pandoc man page source.
This script fetches them (or copies them from a local checkout with --local)
and converts them to pages MkDocs can render: the pandoc title block goes, the
headings are demoted by one level so the page title is the only H1, tab indented
definition lists become space indented ones, and relative links are turned into
links to the upstream repository.

    ./scripts/sync_upstream_docs.py            # fetch from GitHub
    ./scripts/sync_upstream_docs.py --local    # from ../git-ftp and ../git-ftp-py
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "docs" / "reference"

PY_REPO = "https://github.com/git-ftp/git-ftp-py"
SH_REPO = "https://github.com/git-ftp/git-ftp"
PY_RAW = "https://raw.githubusercontent.com/git-ftp/git-ftp-py/main"
SH_RAW = "https://raw.githubusercontent.com/git-ftp/git-ftp/master"


@dataclass
class Source:
    """One upstream document and how to turn it into a page of this site."""

    target: str
    raw_url: str
    local_path: Path
    blob_url: str
    title: str
    nav_title: str
    intro: str
    link_base: str
    drop: list[str] = field(default_factory=list)
    links: dict[str, str] = field(default_factory=dict)


SOURCES = [
    Source(
        target="manual-python.md",
        raw_url=f"{PY_RAW}/docs/git-ftp.1.md",
        local_path=Path("../git-ftp-py/docs/git-ftp.1.md"),
        blob_url=f"{PY_REPO}/blob/main/docs/git-ftp.1.md",
        title="Manual — git-ftp (Python)",
        nav_title="Manual (Python)",
        intro=(
            "The complete manual page of the Python implementation, the one "
            "`git ftp help` and `man git-ftp` show."
        ),
        link_base=f"{PY_REPO}/blob/main",
        links={
            "COMPATIBILITY.md": "compatibility.md",
            "CHANGELOG.md": f"{PY_REPO}/blob/main/CHANGELOG.md",
        },
    ),
    Source(
        target="manual-bash.md",
        raw_url=f"{SH_RAW}/man/git-ftp.1.md",
        local_path=Path("../git-ftp/man/git-ftp.1.md"),
        blob_url=f"{SH_REPO}/blob/master/man/git-ftp.1.md",
        title="Manual — git-ftp (Bash)",
        nav_title="Manual (Bash)",
        intro=(
            "The complete manual page of the original Bash implementation, "
            "the one `git ftp help` and `man git-ftp` show."
        ),
        link_base=f"{SH_REPO}/blob/master",
        drop=[
            r"^This is the manual for version",
            r"^Please consider the \[changelog\]",
            r"^the _Branch > Tags_ select above",
        ],
        links={
            "../CHANGELOG.md": f"{SH_REPO}/blob/master/CHANGELOG.md",
            "../INSTALL.md": "../getting-started/install.md",
        },
    ),
    Source(
        target="compatibility.md",
        raw_url=f"{PY_RAW}/COMPATIBILITY.md",
        local_path=Path("../git-ftp-py/COMPATIBILITY.md"),
        blob_url=f"{PY_REPO}/blob/main/COMPATIBILITY.md",
        title="Compatibility between the implementations",
        nav_title="Compatibility",
        intro=(
            "What the Python port keeps identical to the Bash original, which "
            "of its bugs it fixes, and where it deliberately behaves "
            "differently."
        ),
        link_base=f"{PY_REPO}/blob/main",
    ),
]


def read(source: Source, local: bool) -> str:
    if local:
        path = (ROOT / source.local_path).resolve()
        if not path.is_file():
            sys.exit(f"missing local checkout: {path}")
        return path.read_text(encoding="utf-8")
    with urlopen(source.raw_url, timeout=30) as response:  # noqa: S310 - fixed https URLs
        return response.read().decode("utf-8")


def strip_title_block(text: str) -> str:
    """Remove the leading pandoc title block ("% title" lines)."""
    lines = text.splitlines()
    while lines and (lines[0].startswith("%") or not lines[0].strip()):
        lines.pop(0)
    return "\n".join(lines)


def expand_tabs(line: str) -> str:
    """Turn leading tabs into four spaces each, so code blocks and definition
    list bodies keep their meaning in Python-Markdown."""
    stripped = line.lstrip("\t")
    return "    " * (len(line) - len(stripped)) + stripped


def convert(source: Source, text: str) -> str:
    body = strip_title_block(text)

    out: list[str] = []
    for raw_line in body.splitlines():
        if any(re.search(pattern, raw_line) for pattern in source.drop):
            continue
        line = expand_tabs(raw_line)
        # ":<tab>definition" has become ":    definition"; a definition list
        # marker wants the colon plus a space, with the body on column four.
        line = re.sub(r"^:[ \t]+", ":   ", line)
        # pandoc man source escapes angle brackets and backticks; on the web
        # they should be an entity and a code span.
        line = line.replace("\\<", "&lt;").replace("\\>", "&gt;")
        line = line.replace("\\`", "`")
        # Demote headings so that the page title stays the only level one.
        if line.startswith("#"):
            line = "#" + line
        out.append(line)
    body = "\n".join(out).strip()

    for old, new in source.links.items():
        body = body.replace(f"]({old})", f"]({new})")
    # Anything still pointing at a repository file goes to the repository.
    body = re.sub(
        r"\]\((?!https?:|#|\.\./|[a-z-]+\.md)([A-Za-z0-9_./-]+\.(?:md|sh|1))\)",
        rf"]({source.link_base}/\1)",
        body,
    )

    header = "\n".join(
        [
            "---",
            f"title: {source.title}",
            "---",
            "",
            f"# {source.title}",
            "",
            source.intro,
            "",
            "!!! info \"Synced from upstream\"",
            "",
            f"    This page is generated from [its source]({source.blob_url})",
            "    in the tool's repository and is refreshed every time the site",
            "    is built. Edit it there, not here.",
            "",
        ]
    )
    return f"{header}\n{body}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--local",
        action="store_true",
        help="read from sibling checkouts instead of GitHub",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail instead of writing when a page would change",
    )
    args = parser.parse_args()

    REFERENCE.mkdir(parents=True, exist_ok=True)
    changed = False
    for source in SOURCES:
        page = convert(source, read(source, args.local))
        target = REFERENCE / source.target
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current == page:
            print(f"unchanged  docs/reference/{source.target}")
            continue
        changed = True
        if args.check:
            print(f"OUTDATED   docs/reference/{source.target}")
            continue
        target.write_text(page, encoding="utf-8")
        print(f"written    docs/reference/{source.target}")

    if args.check and changed:
        print("\nRun ./scripts/sync_upstream_docs.py to update.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
