---
title: Continuous deployment
---

# Continuous deployment

git-ftp needs nothing but Git and a network connection, which makes it a
comfortable deploy step in any CI system.

!!! warning "Fetch the whole history"

    Most CI systems clone with `--depth 1`. git-ftp has to diff against the
    commit recorded on the server, and that commit is usually not in a shallow
    clone — the deployment then uploads everything, or fails. Configure a full
    clone, as shown below.

Keep the credentials in the CI system's secret store and pass them through the
environment; never commit them.

## GitHub Actions

```yaml title=".github/workflows/deploy.yml"
name: Deploy

on:
  push:
    branches: [main]

concurrency: deploy   # one deployment at a time

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v7
        with:
          fetch-depth: 0          # git-ftp needs the history

      - uses: actions/setup-python@v7
        with:
          python-version: "3.x"

      - run: pip install git-ftp

      - name: Deploy
        env:
          GIT_FTP_URL: ftp://example.com/public_html
          GIT_FTP_USER: ${{ secrets.FTP_USER }}
          GIT_FTP_PASSWORD: ${{ secrets.FTP_PASSWORD }}
        run: git ftp push --auto-init
```

`--auto-init` uploads everything the first time, so the very first run works
without a manual `git ftp init`.

There is also a ready-made action built on the Bash implementation:
[FTP Deploy](https://github.com/marketplace/actions/ftp-deploy).

## GitLab CI

```yaml title=".gitlab-ci.yml"
deploy:
  stage: deploy
  image: python:3-slim
  variables:
    GIT_DEPTH: 0                  # git-ftp needs the history
  only:
    - main
  before_script:
    - apt-get update && apt-get install -y --no-install-recommends git
    - pip install git-ftp
  script:
    - git ftp push --auto-init
```

Set `GIT_FTP_URL`, `GIT_FTP_USER` and `GIT_FTP_PASSWORD` as masked, protected
CI/CD variables in the project settings.

## Bitbucket Pipelines

```yaml title="bitbucket-pipelines.yml"
image: python:3-slim

clone:
  depth: full                     # git-ftp needs the history

pipelines:
  branches:
    main:
      - step:
          name: Deploy
          deployment: production
          script:
            - apt-get update && apt-get install -y --no-install-recommends git
            - pip install git-ftp
            - git ftp push --auto-init
```

There is a [video walkthrough](https://www.youtube.com/watch?v=8HZhHtZebdw) of
the same setup with the Bash implementation.

## Deploying per environment

If scopes are named after branches, one step covers all of them:

```sh
git ftp push -s          # scope = current branch name
```

See [scopes](scopes.md).

## Things worth adding

- **Serialise deployments.** Two jobs deploying at once corrupt each other's
  state. Use the CI system's concurrency control, and `--lock` as a second net.
- **Build first.** Compile assets in an earlier step and list the results in
  [`.git-ftp-include`](selecting-files.md#uploading-untracked-files).
- **Look before pushing.** A `git ftp push --dry-run` step on pull requests
  shows what a merge would deploy.
- **Fail loudly.** git-ftp's [exit codes](../reference/manual-python.md#exit-codes)
  distinguish a login failure (4) from a locked remote (7) and a hook veto (9).
