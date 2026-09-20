---
title: Troubleshooting
---

# Troubleshooting

Start by asking git-ftp what it is doing:

```sh
git ftp push -v      # what happens, step by step
git ftp push -vv     # everything, including the protocol trace
git ftp push --dry-run
```

## It wants me to run `git ftp init`

```text
Could not get last commit. Network down? Wrong URL? Use 'git ftp init' for the initial push.
```

git-ftp could not read `.git-ftp.log` from the server. Either it really is not
there — then `git ftp init` (or `git ftp catchup`, if the files are already
uploaded) is right — or the server could not be reached at all. The Python
implementation distinguishes the two and tells you which one it is; with the
Bash implementation, check the URL, the credentials and the path first.

If the server forbids files starting with a dot, give the log another name:

```sh
git config git-ftp.deployedsha1file gitftp.log
```

## The connection hangs or times out

Usually the FTP data connection, not the login. Try, in this order:

```sh
git ftp push --disable-epsv     # PASV instead of EPSV
git ftp push --active           # active mode; needs an FTP-aware firewall
```

SFTP has none of these problems, if the server offers it.

## Certificate or host key errors

For FTPS and FTPES with a private or self-signed certificate:

```sh
git ftp push --cacert /path/to/ca.pem
```

For SFTP with the Python implementation, an unknown host key is refused. Add
the server once:

```sh
ssh-keyscan -p 22 example.com >> ~/.ssh/known_hosts
```

`--insecure` skips both checks. It is a last resort, not a fix.

## `Protocol sftp not supported or disabled in libcurl`

The curl in use has no SFTP support — the usual case on macOS with the Bash
implementation. Use the Python implementation, which speaks SFTP through
paramiko, or [build curl with libssh2](../getting-started/install.md#sftp-on-macos-with-the-bash-version).

## Everything gets uploaded every time

The commit recorded on the server is not in your clone, so git-ftp cannot
compute a difference. In CI this is almost always a shallow clone — see
[continuous deployment](ci-cd.md). Locally it happens after a force-push or a
rebase that dropped the deployed commit; `git ftp catchup` on the right commit
sets the state straight.

## Files appear with mangled names

Names containing `%`, `?`, `[`, `]`, `"` or a backslash were mangled by the
Bash implementation on the way into curl. The Python implementation transfers
them intact.

## The password is not accepted

- Quote it in single quotes: `--passwd '#my$fancy!secret'`.
- A password starting with a dash cannot be passed with `--passwd` in the Bash
  implementation; use `git config`, `-P` or `~/.netrc`.
- `-P` asks interactively and avoids all quoting questions.
- Check that no scope is overriding the password: `git config --get-regexp '^git-ftp\.'`.

## A deployment was interrupted and now everything is locked

```text
Fatal: Repository is locked by <user>
```

```sh
git ftp unlock          # Python implementation
git ftp push --force    # ignore the lock
```

The lock file is `git-ftp.lck` in the deployment directory; deleting it by hand
works too.

## The uploaded files do not match the commit

Something edited the working tree while the upload ran. Deploy from a
consistent snapshot instead:

```sh
git ftp push --worktree            # Python implementation
```

## Large files are uploaded as text stubs

With Git LFS, git-ftp uploads what Git tracks, which is the pointer file. Fetch
the real contents first:

```sh
git lfs pull
git ftp push
```

## Exit codes

| Code | Meaning |
|---|---|
| 0 | success |
| 1 | unexpected error |
| 2 | wrong usage |
| 3 | missing argument |
| 4 | error while uploading (also: remote unreachable, login failed) |
| 5 | error while downloading (also: `push` before `init`) |
| 6 | unknown protocol |
| 7 | remote locked |
| 8 | Git error — not a repository, dirty working tree, bad branch |
| 9 | hook failed |
| 10 | local filesystem error |
| 130 | interrupted |

## Still stuck?

Open an issue with the output of `git ftp push -vv`, with credentials removed:

- [git-ftp (Python) issues](https://github.com/git-ftp/git-ftp-py/issues)
- [git-ftp (Bash) issues](https://github.com/git-ftp/git-ftp/issues)
