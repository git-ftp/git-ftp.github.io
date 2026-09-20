---
title: Downloading from the server
---

# Downloading from the server

Sometimes the server is ahead: someone edited a file over FTP, or a CMS wrote
something. Three actions bring that back into your repository.

!!! warning "These actions change your working tree"

    They delete local files that are not on the server, except ignored files,
    `.git` and git-ftp's own files. Commit or stash your work first, and make
    sure `.git-ftp-ignore` covers what must stay.

    In the Bash implementation these actions are experimental and need
    [`lftp`](https://lftp.yar.ru/) installed. The Python implementation does it
    itself.

## download

```sh
git ftp download
```

Mirrors the remote directory into the working tree and stops there, so you can
inspect the result with `git diff`. It refuses to run while the working tree
has untracked files.

## pull

`git ftp download` compares against whatever you have checked out, which is the
wrong baseline if you have local commits that were never deployed. `pull` uses
the deployed commit instead:

```sh
git ftp pull
```

It does the equivalent of:

```sh
git checkout <deployed-commit>
git ftp download
git add --all
git commit -m '[git-ftp] remotely untracked modifications'
git ftp catchup
git checkout <my-branch>
git merge <new-remote-commit>
```

To look at the merge before it is committed:

```sh
git ftp pull --no-commit
# inspect, then
git commit
# or
git merge --abort
```

After an abort the downloaded changes live on in an unreferenced commit until
Git's garbage collector runs. The commit id is printed, so you can tag it or
branch from it.

`--changed-only` limits the transfer to files that also changed locally.

## snapshot

To turn a server that has never seen git-ftp into a repository:

```sh
git ftp snapshot ftp://example.com/public_html projects/example
```

Downloads the remote directory into a new repository, commits it and records
that commit on the server, so the next `git ftp push` behaves as if you had run
`init`.
