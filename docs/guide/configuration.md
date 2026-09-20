---
title: Configuration
---

# Configuration

Every option can be stored, so that a deployment is just `git ftp push`.

## Where settings come from

git-ftp reads a setting from the first source that has it:

1. the command line;
2. the environment — `GIT_FTP_URL`, `GIT_FTP_USER`, `GIT_FTP_PASSWORD`
   (Python implementation only);
3. `.git-ftp-config` in the repository root, if present;
4. the Git configuration, scope keys (`git-ftp.<scope>.<key>`) before plain
   keys (`git-ftp.<key>`).

`.git/config` is local to your clone, so credentials put there are not
committed. `.git-ftp-config` *is* part of the repository — keep passwords out
of it.

## Setting defaults

```sh
git config git-ftp.url "ftp://example.com/public_html"
git config git-ftp.user "alice"
git config git-ftp.password "s3cret"
```

After that:

```sh
git ftp push
```

## The keys

| Key | Meaning |
|---|---|
| `git-ftp.url` | Server URL, for example `ftp://example.com/public_html` |
| `git-ftp.user` | Login name |
| `git-ftp.password` | Password |
| `git-ftp.password-command` | Command whose first output line is the password :material-language-python: |
| `git-ftp.keychain` | macOS keychain entry, `account@host` |
| `git-ftp.syncroot` | Deploy only this directory, as if it were the repository root |
| `git-ftp.remote-root` | Remote directory to deploy into, replacing the URL's path |
| `git-ftp.deployedsha1file` | Name of the log file on the server (default `.git-ftp.log`) |
| `git-ftp.branch` | Branch to deploy |
| `git-ftp.insecure` | Do not verify TLS certificates or SFTP host keys |
| `git-ftp.cacert` | CA certificate bundle for FTPS/FTPES |
| `git-ftp.key` / `git-ftp.pubkey` | SFTP private and public key file |
| `git-ftp.key-passphrase` | Passphrase of an encrypted SFTP key :material-language-python: |
| `git-ftp.disable-epsv` | Use PASV instead of EPSV |
| `git-ftp.proxy` | Proxy URL |
| `git-ftp.jobs` | Number of parallel connections, default 4 :material-language-python: |
| `git-ftp.worktree` | Upload from a throwaway worktree :material-language-python: |
| `git-ftp.no-commit` | `pull` merges without committing |

:material-language-python: — Python implementation only.

Booleans are read the way `git config` reads them: `true`, `yes`, `on`, `1`
against `false`, `no`, `off`, `0`.

## A config file in the repository

Instead of `git config`, the same keys can live in `.git-ftp-config` in the
repository root, which takes precedence over the Git configuration:

```ini
[git-ftp]
    url = ftp://example.com/public_html
    user = alice
    syncroot = public
    jobs = 8
```

This is the place for settings that belong to the project rather than to your
machine. Credentials belong in `.git/config`, in the environment or in a
password manager — see [credentials](protocols.md#credentials).

## Environment variables

The Python implementation reads `GIT_FTP_URL`, `GIT_FTP_USER` and
`GIT_FTP_PASSWORD` after the command line and before the Git configuration,
which is what you want in CI:

```sh
GIT_FTP_URL="ftp://example.com/htdocs" \
GIT_FTP_USER="$FTP_USER" \
GIT_FTP_PASSWORD="$FTP_PASSWORD" \
git ftp push
```

Nothing is written to a file and no password appears on a command line.

## The log file on the server

git-ftp stores the deployed commit id in `.git-ftp.log` in the deployment
directory. Some hardened FTP servers refuse to write names starting with a dot;
give the file another name then:

```sh
git config git-ftp.deployedsha1file gitftp.log
```

Both implementations use the same file, so changing the name affects any
machine deploying this repository.

## Consistent uploads while editing

git-ftp reads the files it uploads from the working tree. If you edit them
while a long deployment runs, the server can end up with contents that do not
match the commit.

The Python implementation can read them from a throwaway Git worktree checked
out at the commit being deployed instead:

```sh
git ftp push --worktree
git config git-ftp.worktree true     # or always
```

The worktree shares the object store, so only a working copy is written to
disk, and it is removed when the deployment finishes. Untracked files added
through `.git-ftp-include` are not part of the commit and are still read from
the live working tree.

## Parallel transfers

The Python implementation uses four connections at once. Change that per run or
per repository:

```sh
git ftp push --jobs 8
git config git-ftp.jobs 1     # sequential, like the Bash version
```

Uploads run first, then deletes, and the log is written last, only when every
upload succeeded. The first failed upload stops the deployment with exit
code 4 and leaves the log untouched; a failed delete is a warning. Ctrl-C stops
promptly and exits with 130.
