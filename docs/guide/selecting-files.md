---
title: Selecting files
---

# Selecting files

By default git-ftp uploads every file Git tracks. Three mechanisms change that:
`.git-ftp-ignore` removes files, `.git-ftp-include` adds untracked ones and
`--syncroot` deploys a subdirectory.

## Ignoring files

Put shell glob patterns into `.git-ftp-ignore` in the repository root, one per
line. Matching files are never uploaded and never deleted on the server.

```text
config/*
*.txt
foobar.txt
.gitignore
*/.gitkeep
.git-ftp-ignore
.git-ftp-include
.gitlab-ci.yml
```

Two details differ from `.gitignore`:

- `*` also matches `/`, so `config/*` covers everything below `config/`;
- a pattern has to match the **whole** path, not a part of it. To catch a file
  in any directory, write `*/.gitkeep`, not `.gitkeep`.

Paths are the Git paths, including the syncroot if one is set.

!!! note "Since version 1.1.0"

    Older Bash versions interpreted the patterns as regular expressions.
    Everything current treats them as globs.

## Uploading untracked files

Build output is often not in Git but still has to reach the server.
`.git-ftp-include` lists those files.

**Always upload a file** — prefix it with `!`:

```text
!VERSION.txt
```

**Upload a file when a tracked file changed** — `target:source`:

```text
css/style.css:scss/style.scss
```

Whenever `scss/style.scss` changed since the deployed commit, `css/style.css`
is uploaded. List several sources for the same target if more than one can
trigger it:

```text
css/style.css:scss/style.scss
css/style.css:scss/mixins.scss
```

**Upload a whole directory** — a target ending in `/`:

```text
vendor/:composer.lock
```

Everything below `vendor/` is uploaded whenever `composer.lock` changed. Note
that this uploads all of it, including files already on the server, and never
deletes anything from that directory.

If the target is missing locally, a change to its source deletes it on the
server.

Paths are relative to the Git working directory. With `--syncroot`, the
**source** (right of the colon) is relative to the syncroot:

```text
# syncroot "html": upload html/style.css when html/style.scss changed
html/style.css:style.scss
```

Prefix the source with `/` to point outside the syncroot, relative to the
repository root:

```text
# syncroot "dist": upload dist/style.css when src/style.scss changed
dist/style.css:/src/style.scss
```

Include rules are applied first, ignore patterns afterwards — an ignored file
stays ignored even if an include rule names it.

## Deploying a subdirectory

If only one directory belongs on the server, and it should become the server's
root:

```sh
git ftp push --syncroot public
git config git-ftp.syncroot public    # or once and for all
```

`public/index.html` then lands as `index.html` on the server.

`--remote-root` is the counterpart on the other side: it sets the directory to
deploy **into**, replacing the path of the URL.

```sh
git ftp push --remote-root htdocs
```

## Checking what will happen

`--dry-run` prints the plan and transfers nothing:

```sh
git ftp push --dry-run
```

Other useful selections:

```sh
git ftp push -a              # upload everything, not only the changes
git ftp push -c 1f2a3b4      # treat this commit as the deployed one
git ftp push -b staging      # deploy another branch
```
