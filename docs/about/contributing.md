---
title: Contributing
---

# Contributing

Both implementations are maintained on GitHub, and both take patches.

<div class="grid cards" markdown>

-   :fontawesome-brands-python: **[git-ftp-py][py]**

    ---

    The Python implementation.

    [Issues][py-issues] · [Pull requests][py-prs] · [Changelog][py-changelog]

-   :material-bash: **[git-ftp][sh]**

    ---

    The original Bash implementation.

    [Issues][sh-issues] · [Pull requests][sh-prs] · [Changelog][sh-changelog]

</div>

## Reporting a bug

Include the command you ran, the output of `git ftp push -vv` with credentials
removed, the version (`git ftp --version`) and the server software if you know
it. FTP servers differ wildly in what they accept, so naming yours often solves
the riddle straight away.

## Working on the Python implementation

```sh
git clone https://github.com/git-ftp/git-ftp-py.git
cd git-ftp-py
uv sync --all-groups
make lint typecheck test     # ruff, mypy, pytest
make test-docker             # against pure-ftpd containers, Linux only
```

The test suite starts real FTP, FTPS and SFTP servers in-process, so most
changes can be covered by a test without any server of your own. The manual
page source is `docs/git-ftp.1.md`.

Anything that changes behaviour compared to the Bash original belongs in
`COMPATIBILITY.md` — that file is the contract between the two implementations
and is published [here](../reference/compatibility.md).

## Working on the Bash implementation

```sh
git clone https://github.com/git-ftp/git-ftp.git
cd git-ftp
make test
```

The core functionality is unit tested with
[shunit2](https://github.com/kward/shunit2); the tests are in `tests/`. The
manual page source is `man/git-ftp.1.md`.

Add yourself to the [AUTHORS](https://github.com/git-ftp/git-ftp/blob/master/AUTHORS)
file with your first patch.

## This website

The site is built with [MkDocs](https://www.mkdocs.org/) and
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) from the
[git-ftp.github.io](https://github.com/git-ftp/git-ftp.github.io) repository
and published by GitHub Pages on every push.

```sh
git clone https://github.com/git-ftp/git-ftp.github.io.git
cd git-ftp.github.io
uv sync
uv run mkdocs serve
```

The three reference pages are generated from the tool repositories by
`scripts/sync_upstream_docs.py` and refreshed at build time — fix a manual page
upstream, not here. Everything else under `docs/` is written by hand; there is
an :material-pencil: link at the top of every page that takes you straight to
its source.

[py]: https://github.com/git-ftp/git-ftp-py
[py-issues]: https://github.com/git-ftp/git-ftp-py/issues
[py-prs]: https://github.com/git-ftp/git-ftp-py/pulls
[py-changelog]: https://github.com/git-ftp/git-ftp-py/blob/main/CHANGELOG.md
[sh]: https://github.com/git-ftp/git-ftp
[sh-issues]: https://github.com/git-ftp/git-ftp/issues
[sh-prs]: https://github.com/git-ftp/git-ftp/pulls
[sh-changelog]: https://github.com/git-ftp/git-ftp/blob/master/CHANGELOG.md
