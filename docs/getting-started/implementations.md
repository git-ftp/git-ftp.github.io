---
title: Which implementation
---

# Which implementation

git-ftp exists twice: as the original Bash script and as a native Python port.
Both deploy the same way and can take over from each other at any time.

## Short answer

Install the **Python** implementation unless you have a reason not to:

```sh
pip install git-ftp
```

It transfers files in parallel, needs no `lftp` for downloading, verifies SFTP
host keys, keeps passwords out of the process list and fixes a long list of
[upstream bugs](../reference/compatibility.md#upstream-bugs-that-are-fixed).

Use the **Bash** implementation when Python is inconvenient — a minimal
container, a shared host where only a shell script may be dropped into `bin`,
or a system whose distribution already packages `git-ftp` and where that is the
easiest thing to audit.

## Side by side

| | git-ftp (Python) | git-ftp (Bash) |
|---|---|---|
| Source | [git-ftp/git-ftp-py][py] | [git-ftp/git-ftp][sh] |
| Install | `pip install git-ftp` | distribution package or one script |
| Runtime | Python 3.10+, `git` | POSIX shell, `curl`, `git` |
| FTP, FTPS, FTPES | libcurl through pycurl | curl |
| SFTP | paramiko, host keys verified | curl, host key not checked |
| Transfers | parallel, `--jobs` (default 4) | one file after another |
| `download`, `pull`, `snapshot` | built in | needs `lftp` installed |
| Passwords | passed to libcurl in memory | may appear in the process list |
| Encrypted SSH keys | `--key-passphrase`, prompt, `ssh-agent` | not supported |
| Progress | spinner with a done/total count on a terminal | plain lines |
| `--worktree` | yes — edits during upload cannot leak in | no |
| Shell completion | bash, zsh, fish | no |

## What they share

The port's rule is that everything on the wire and in configuration stays
identical:

- the deployed-commit file `.git-ftp.log`, at the same place with the same
  content;
- the `git-ftp.*` configuration keys, the scope keys and `.git-ftp-config`,
  with the same precedence;
- `.git-ftp-ignore` and `.git-ftp-include`, with the same glob and
  `target:source` semantics;
- the `pre-ftp-push` and `post-ftp-push` hooks, with the same arguments and
  stdin format;
- the exit codes and the progress messages.

So you can deploy with the Bash script today and with the Python program
tomorrow, from another machine, without touching the server.

The full list of what is identical, what was fixed and what deliberately
differs is on the [compatibility page](../reference/compatibility.md).

## Switching

There is nothing to migrate. Install the other implementation and run
`git ftp push` — it reads the same configuration and the same remote log. If
you want to be sure first:

```sh
git ftp push --dry-run
```

[py]: https://github.com/git-ftp/git-ftp-py
[sh]: https://github.com/git-ftp/git-ftp
