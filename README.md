# git-ftp.github.io

The documentation site for both git-ftp implementations,
[git-ftp-py](https://github.com/git-ftp/git-ftp-py) (Python) and
[git-ftp](https://github.com/git-ftp/git-ftp) (Bash), published at
<https://git-ftp.github.io>.

Built with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
and deployed by GitHub Pages on every push to `master`.

## Working on it

```sh
uv sync
uv run mkdocs serve      # http://127.0.0.1:8000
uv run mkdocs build --strict
```

## Where the content lives

Everything under `docs/` is written by hand, except the three pages in
`docs/reference/`. Those are generated from the manual pages in the tool
repositories:

| Page | Source |
|---|---|
| `reference/manual-python.md` | `git-ftp-py:docs/git-ftp.1.md` |
| `reference/manual-bash.md` | `git-ftp:man/git-ftp.1.md` |
| `reference/compatibility.md` | `git-ftp-py:COMPATIBILITY.md` |

```sh
uv run scripts/sync_upstream_docs.py            # fetch from GitHub
uv run scripts/sync_upstream_docs.py --local    # from ../git-ftp, ../git-ftp-py
uv run scripts/sync_upstream_docs.py --check    # fail if they are outdated
```

The deploy workflow runs the sync before every build, and once a day on a
schedule, so a manual page fixed upstream appears here without a commit in this
repository. Fix those pages upstream, not here.

## Deployment

`.github/workflows/deploy.yml` builds the site and publishes it with
`actions/deploy-pages`. This needs **Settings → Pages → Source: GitHub
Actions** in the repository settings; no `gh-pages` branch is involved.
`.github/workflows/build.yml` builds pull requests without deploying.
