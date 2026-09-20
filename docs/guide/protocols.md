---
title: Protocols and credentials
---

# Protocols and credentials

## The URL

```text
protocol://host.domain.tld:port/path
```

```sh
git ftp push ftp://host.example.com:2121/mypath
```

| URL | Transport | Encryption |
|---|---|---|
| `ftp://host/path` | curl / libcurl | none — the password crosses the network in clear |
| `ftpes://host/path` | curl / libcurl | explicit TLS (`AUTH TLS`) |
| `ftps://host/path` | curl / libcurl | implicit TLS, usually port 990 |
| `sftp://host/path` | curl (Bash) / paramiko (Python) | SSH |

`ftp://` is the default when no protocol is given, and `host:port/path` without
a scheme is understood as FTP.

Credentials may be part of the URL — `ftp://alice:s3cret@example.com/htdocs` —
which is how `add-scope` stores them. The Python implementation never prints
them back or passes them on a command line.

!!! tip "Prefer an encrypted protocol"

    Plain FTP sends the password and every file unencrypted. If the server
    offers FTPES or SFTP, use it.

## SFTP paths

Relative and absolute paths are not the same thing over SSH:

```sh
sftp://example.com/public_html      # relative to the login directory
sftp://example.com/~/public_html    # relative to the home directory
sftp://example.com//var/www         # absolute
```

## SFTP keys and host keys

```sh
git ftp push -u alice --key ~/.ssh/id_ed25519 sftp://example.com/~/public_html
```

The public key is guessed as `<key>.pub`; `--pubkey` sets it explicitly. The
Python implementation also takes `--key-passphrase` for an encrypted key, asks
for the passphrase interactively, and uses a running `ssh-agent`
(`SSH_AUTH_SOCK`) if there is one.

It verifies the server's host key against `~/.ssh/known_hosts` and
`/etc/ssh/ssh_known_hosts`. Add an unknown server first:

```sh
ssh-keyscan -p 22 example.com >> ~/.ssh/known_hosts
```

The Bash implementation accepts any host key silently.

## TLS certificates

Certificates are verified. For a private CA:

```sh
git ftp push --cacert /etc/ssl/certs/ca.pem
```

`--insecure` turns verification off — for TLS certificates and, in the Python
implementation, for SFTP host keys as well. It leaves you open to a
man-in-the-middle, but it is still better than plain FTP.

## Passive, active, EPSV

FTP data connections default to EPSV. Depending on the network that can fail:

```sh
git ftp push --disable-epsv     # use PASV
git ftp push --active           # the original active mode
```

Neither applies to SFTP. A proxy is passed through with `-x`:

```sh
git ftp push -x http://proxy.example.com:3128
```

## Credentials

There are more ways to hand over a password than putting it into the config.

### Ask interactively

```sh
git ftp push -u alice -P ftp://example.com/htdocs
```

### From a password manager

The Python implementation runs a command and uses the first line of its output:

```sh
git config git-ftp.password-command "pass show example.com/ftp"
```

### From the environment

```sh
GIT_FTP_USER=alice GIT_FTP_PASSWORD="$SECRET" git ftp push
```

### From `~/.netrc`

Both implementations fall back to `~/.netrc` when no user is given:

```text
machine ftp.example.com
login alice
password SECRET
```

```sh
git ftp init ftp.example.com
```

### From the macOS keychain

```sh
git ftp init --keychain account@host ftpes://host
git config git-ftp.keychain alice@example.com
```

Without a value, the account and host are guessed from the user and the URL.
Add an entry like this — the entry has to be an *internet* password, not the
generic one the Keychain Access app creates:

```sh
security add-internet-password -a alice -r "ftp " -s example.com -w secr3t
```

`-r` is the protocol and must be exactly four characters: `"ftp "` for FTP and
for SSH with password authentication, `ftps` for FTPS and FTPES. The keychain
cannot unlock a password-protected SSH key.

### Passwords with special characters

Quote them, in single quotes:

```sh
git ftp push --passwd '#my$fancy!secret'
git config git-ftp.password '#my$fancy!secret'
```

A password starting with a dash defeats quoting in the Bash implementation
([by design](https://github.com/git-ftp/git-ftp/issues/468)); use `git config`,
`-P` or `~/.netrc` instead. The Python implementation accepts it as
`-p=-secret`.

!!! danger "Passwords on the command line"

    Anything in `argv` is visible to other users through `ps`. The Bash
    implementation also hands the password to curl that way. Prefer `-P`,
    `--password-command`, the environment or `~/.netrc` on shared machines.
