---
title: Compatibility between the implementations
---

# Compatibility between the implementations

What the Python port keeps identical to the Bash original, which of its bugs it fixes, and where it deliberately behaves differently.

!!! info "Synced from upstream"

    This page is generated from [its source](https://github.com/git-ftp/git-ftp-py/blob/main/COMPATIBILITY.md)
    in the tool's repository and is refreshed every time the site
    is built. Edit it there, not here.

## Compatibility with git-ftp 1.6.0

This Python git-ftp is a port of the Bash [git-ftp](https://github.com/git-ftp/git-ftp),
version 1.6.0. The rule of the port is: **keep everything on the wire and in
configuration identical, fix the bugs, and write down every deviation here.**

A remote deployed with the Bash git-ftp can be picked up by this port and vice
versa. The deployed-commit file (`.git-ftp.log`), its content, the config keys,
the `.git-ftp-ignore` and `.git-ftp-include` formats, the hook names and
arguments, the exit codes and the default progress messages are unchanged.

### Unchanged

| Area | Status |
|---|---|
| Actions `init`, `push`, `catchup`, `show`, `log`, `download`, `pull`, `snapshot`, `add-scope`, `remove-scope`, `help`, `version` | Same names, same semantics |
| Options | Every 1.6.0 option is accepted with the same spelling |
| Config keys `git-ftp.*` and `git-ftp.<scope>.*`, `.git-ftp-config` | Same keys, same precedence, an explicit empty value still overrides |
| `.git-ftp.log` (or `git-ftp.deployedsha1file`) | Same location and content (commit id plus newline) |
| `.git-ftp-ignore` | Same glob semantics: `*` crosses `/`, patterns match the whole Git path including the syncroot |
| `.git-ftp-include` | Same `!target` and `target:source` forms, same directory/missing-target rules, applied before ignore |
| Hooks `pre-ftp-push`, `post-ftp-push` | Same arguments and stdin format |
| Exit codes | 2 usage, 3 missing argument, 4 upload, 5 download, 6 unknown protocol, 7 locked, 8 git, 9 hook, 10 filesystem |
| Progress output | `N file(s) to sync:`, `[i of N] Buffered for upload '…'.`, `Uploading ...`, `Last deployment changed from … to ….`, etc. |
| `~/.netrc` fallback when no user is given | Same, now also for sftp |
| Remote lock semantics | Same file (`git-ftp.lck`), checked and written only with `--lock`, same "a lock for my own commit is mine" rule |
| Empty remote directories | Kept, as upstream since 1.1.0 (issue #168) |

### Upstream bugs that are fixed

These are behaviours of the Bash script that are clearly unintended. Each is
fixed rather than reproduced.

- `--no-verify` and `--enable-post-errors` swallowed the argument after them.
- `--key=FILE`, `--pubkey=FILE` and `--branch=NAME` were not parsed.
- `--silent` also suppressed fatal error messages, and `-v` sent them to stdout.
  Fatal errors now always go to stderr, at every verbosity.
- `--remote-root` was prepended to the URL's path although the manual says it
  replaces it. It replaces it.
- `--lock` toggled: giving it twice turned locking off. It is a plain flag.
- The lock file's two lines were joined by a literal `\n`. A real newline is
  written; both forms are read.
- The lock file was named after the script's own file name. The name is fixed.
- `ftp://user@host/path` took `user` for the host. Userinfo in a URL is parsed
  as credentials.
- `host:2121/path` without a scheme was rejected as an unknown protocol even
  though the built-in help shows that form. It is accepted as ftp.
- `add-scope` gave up on a URL whose password contained a colon or an at-sign.
- File names containing `%`, `?`, `[`, `]`, `"` or a backslash were mangled on
  the way into curl. They are transferred intact. So is a file named `-`.
- `git-ftp.no-commit false` enabled the option. Booleans are parsed as Git
  parses them (`true/yes/on/1` and `false/no/off/0`).
- A push whose remote log could not be read for *any* reason said
  "use 'git ftp init'". That message is now reserved for a genuinely missing
  log; a wrong password or an unreachable host is reported as what it is.
- The delete phase ran a directory listing of the remote root just to have a
  transfer to attach `-Q` commands to. Deletes are plain `DELE` commands.
- Files whose type changed (a file becoming a symlink or vice versa, `T` in
  `git diff`) were never uploaded. They are.
- Running from a subdirectory of the repository resolved `--syncroot` and the
  submodule list against the wrong directory.
- `catchup` with more than one submodule only handled the first one, and
  `cd`-ed deeper with every iteration.
- Passwords were visible on the curl command line (`ps`). Credentials are
  passed to libcurl in memory and never appear in URLs, logs or argv.
- Temporary files were left behind on Ctrl-C. There are no temporary files.

### New

- **Parallel transfers**: `--jobs N` / `git-ftp.jobs` (default 4, `1` is
  sequential). Uploads run first, then deletes, and the commit log is written
  last, only when every upload succeeded. The first failed upload stops the
  deploy (exit 4); failed deletes are warnings, as upstream.
- Native `download`, `pull` and `snapshot`: no `lftp` needed. Listings use
  `MLSD` with a `LIST` fallback; downloads are parallel too.
- Submodules are deployed in-process (no recursive `git-ftp` invocation).
- Environment variables `GIT_FTP_URL`, `GIT_FTP_USER`, `GIT_FTP_PASSWORD`,
  read after the command line and before Git configuration.
- `--password-command` / `git-ftp.password-command`: a shell command whose
  first output line is the password.
- `unlock` action to remove a stale lock left by an interrupted deploy.
- `--key-passphrase` / `git-ftp.key-passphrase`, and an interactive prompt,
  for encrypted SFTP keys. Upstream cannot use an encrypted key at all.
- SFTP authentication through a running `ssh-agent` (`SSH_AUTH_SOCK`).
- `--password` as an alias of `--passwd`; `--no-post-hooks`.
- Ctrl-C stops the transfers promptly and exits with 130.
- `version -v` prints the libcurl and paramiko versions in use.
- An interactive terminal shows a progress spinner with a `done/total` count
  while files upload, delete or download; it renders on stderr and is silent
  when output is not a terminal or under `-n`.
- `--worktree` / `git-ftp.worktree`: `init` and `push` read the upload from a
  temporary Git worktree checked out at the deployed commit, so edits to the
  working tree during the upload cannot leak in. Untracked files added by
  `.git-ftp-include` are read from the live working tree, since a worktree of the
  commit cannot contain them.

### Behaviour that differs on purpose

- **SFTP host keys are verified** against `~/.ssh/known_hosts` and
  `/etc/ssh/ssh_known_hosts`. Upstream accepted any host key silently. An
  unknown host is refused with a pointer to `ssh-keyscan`; `--insecure` turns
  verification off, as it does for TLS.
- **SFTP is spoken by paramiko**, not libcurl. FTP, FTPS and FTPES use libcurl
  through pycurl.
- **`git` is required** at run time (the port shells out to it, as upstream).
- A valueless boolean key such as a bare `insecure` line in `.git-ftp-config`
  reads as **true**, exactly as `git config` reads it.
- Diagnostics printed with `-v` go to stderr with a timestamp; progress lines
  stay on stdout. Warnings (`WARNING: …`) go to stderr at every verbosity.
- `ftps://` and `ftpes://` require TLS 1.2 or newer and encrypt the data
  connection as well as the control connection.
- `-u`, `-s` and `-k` without an argument work as upstream (local user, current
  branch, default keychain item). An action name after a bare flag (`-u push`)
  is recognised as the action.
- The `Insecure is 'N'.` and `Disable EPSV is '1'.` diagnostics are printed
  once per repository (twice with one submodule), as upstream.
- `download --changed-only` uses the deployed commit to pick the files
  (upstream ignored the flag for `download`).
- The macOS keychain is read through the `security` command on macOS and
  ignored elsewhere, as upstream. Keychain entries cannot unlock SSH keys.

### Not implemented

- `download`, `pull` and `snapshot` never print lftp's transfer log; they print
  a one-line summary instead (`Downloaded N file(s), deleted M local file(s).`).
