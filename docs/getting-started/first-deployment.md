---
title: First deployment
---

# First deployment

## 1. Tell git-ftp where the server is

Run this once inside your repository:

```sh
git config git-ftp.url "ftp://example.com/public_html"
git config git-ftp.user "alice"
git config git-ftp.password "s3cret"
```

The settings land in `.git/config`, which is not part of the repository, so the
password is not committed. If you would rather not store it at all, see
[credentials](../guide/protocols.md#credentials) for `-P`, `--password-command`,
`~/.netrc`, the macOS keychain and environment variables.

## 2. Upload everything once

If the server is empty, or its contents should be replaced by what is in Git:

```sh
git ftp init
```

This uploads every tracked file that is not ignored and writes the commit id
into `.git-ftp.log` on the server.

If the files are **already** on the server and match your working tree, do not
upload them again — just record the commit:

```sh
git ftp catchup
```

!!! tip "Look before you leap"

    `--dry-run` prints what would be transferred and touches nothing:

    ```sh
    git ftp init --dry-run
    ```

## 3. Deploy your changes

From now on, every deployment is one command:

```sh
echo "new content" >> index.txt
git commit index.txt -m "Add new content"
git ftp push
```

```text
1 file to sync:
[1 of 1] Buffered for upload 'index.txt'.
Uploading ...
Last deployment changed from 1f2a3b4 to ded01b2.
```

git-ftp reads the commit recorded on the server, diffs it against `HEAD` and
transfers exactly the files that were added, changed or deleted. Only when
every upload succeeded does it update the log, so an interrupted deployment
never claims a commit it did not finish.

## 4. Check what is deployed

```sh
git ftp show     # git show of the deployed commit
git ftp log      # git log starting at the deployed commit
```

## Going back, and other branches

Because the state on the server is just a commit, moving around in history is
ordinary Git work:

```sh
# deploy the state of three commits ago
git checkout HEAD~3
git ftp push

# deploy another branch without checking it out
git ftp push -b staging

# upload the difference between develop and master
git checkout develop
git ftp push --commit master
```

## Where to go next

- [Configuration](../guide/configuration.md) — every setting, and where to put it.
- [Scopes](../guide/scopes.md) — staging and production in one repository.
- [Selecting files](../guide/selecting-files.md) — `.git-ftp-ignore`,
  `.git-ftp-include`, `--syncroot`.
- [Continuous deployment](../guide/ci-cd.md) — deploy from GitHub Actions,
  GitLab CI or Bitbucket Pipelines.
