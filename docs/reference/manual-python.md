---
title: Manual — git-ftp (Python)
---

# Manual — git-ftp (Python)

The complete manual page of the Python implementation, the one `git ftp help` and `man git-ftp` show.

!!! info "Synced from upstream"

    This page is generated from [its source](https://github.com/git-ftp/git-ftp-py/blob/main/docs/git-ftp.1.md)
    in the tool's repository and is refreshed every time the site
    is built. Edit it there, not here.

## NAME

git-ftp - Git powered FTP, FTPS, FTPES and SFTP client

## SYNOPSIS

*git-ftp* &lt;action&gt; [&lt;options&gt;] [&lt;url&gt;]

## DESCRIPTION

This manual page documents *git-ftp*, a Python program that uploads the
files of a Git repository to a server over FTP, FTPS, FTPES or SFTP. Only the
files that changed since the last deployment are transferred. The deployed
commit is recorded in a file on the server, *.git-ftp.log* by default, so no
software has to be installed on the server.

Git runs the program as *git ftp* when *git-ftp* is on the PATH.

## ACTIONS

*init*
:   Uploads all tracked files that are not ignored and records the commit in
    *.git-ftp.log* on the server. Fails when the server already has a log.

*catchup*
:   Only creates or updates *.git-ftp.log* on the server. Use it when the
    server already holds the current files.

*push*
:   Uploads the files added or changed and deletes the files removed since the
    deployed commit, then updates *.git-ftp.log*. With *--auto-init* a missing
    log behaves like *init*.

*download*
:   Mirrors the remote directory into the working tree (files missing on the
    server are removed locally; ignored files are left alone). Refuses to run
    while the working tree has untracked files.

*pull*
:   Checks out the deployed commit, downloads the remote changes into a
    commit, records that commit on the server and merges it into the current
    branch.

*snapshot* [&lt;directory&gt;]
:   Downloads a remote directory that is not yet managed by git-ftp into a new
    repository, commits it and records the commit on the server.

*show*
:   Runs *git show* on the deployed commit.

*log*
:   Runs *git log* on the deployed commit.

*add-scope* &lt;scope&gt; &lt;url&gt;
:   Stores the URL (and the credentials contained in it) under a scope name in
    the repository's Git configuration.

*remove-scope* &lt;scope&gt;
:   Removes a scope from the Git configuration.

*unlock*
:   Removes a stale remote lock left by an interrupted deploy.

*help*
:   Prints the built-in help.

*version*
:   Prints the version; with *-v* also the libcurl and paramiko versions.

## OPTIONS

*-u [&lt;username&gt;]*, *--user [&lt;username&gt;]*
:   FTP login name. Without a value the local user name is used.

*-p &lt;password&gt;*, *--passwd &lt;password&gt;*, *--password &lt;password&gt;*
:   FTP password. A value starting with a dash is accepted (*-p=-secret*).

*-P*, *--ask-passwd*
:   Ask for the password interactively.

*--password-command &lt;command&gt;*
:   Run a shell command and use the first line of its output as the password.

*-k [[&lt;account&gt;]@[&lt;host&gt;]]*, *--keychain [[&lt;account&gt;]@[&lt;host&gt;]]*
:   Read the password from the macOS keychain (ignored on other systems).

*-a*, *--all*
:   Upload all files instead of only the changed ones.

*-c &lt;commit&gt;*, *--commit &lt;commit&gt;*
:   Treat the given commit as the deployed one instead of reading the log.

*-A*, *--active*
:   Use FTP active mode.

*-b [&lt;branch&gt;]*, *--branch [&lt;branch&gt;]*
:   Deploy the given branch and switch back afterwards.

*-s [&lt;scope&gt;]*, *--scope [&lt;scope&gt;]*
:   Use the configuration of the given scope. Without a value the current
    branch name is the scope.

*-l*, *--lock*
:   Write a lock file on the server for the duration of the deploy.

*-D*, *--dry-run*
:   Print what would be transferred without transferring anything.

*-f*, *--force*
:   Skip the lock check and the question about an unknown deployed commit.

*-n*, *--silent*
:   Print nothing but fatal errors.

*-v*, *--verbose*
:   Print diagnostics on stderr. *-vv* also prints the protocol trace.

*-j &lt;n&gt;*, *--jobs &lt;n&gt;*
:   Number of parallel connections (default 4). *1* transfers sequentially.

*--remote-root &lt;directory&gt;*
:   Remote directory to deploy into, replacing the path of the URL.

*--syncroot &lt;directory&gt;*
:   Deploy only this directory; it becomes the remote root.

*--key &lt;file&gt;*
:   SFTP private key.

*--pubkey &lt;file&gt;*
:   SFTP public key (defaults to *&lt;key&gt;.pub*).

*--key-passphrase &lt;text&gt;*
:   Passphrase of an encrypted SFTP private key.

*--insecure*
:   Do not verify TLS certificates or SFTP host keys.

*--cacert &lt;file&gt;*
:   CA certificate bundle used to verify FTPS/FTPES servers.

*--disable-epsv*
:   Use PASV instead of EPSV.

*-x &lt;url&gt;*, *--proxy &lt;url&gt;*
:   Proxy URL (also read from *git-ftp.proxy* and *http.proxy*).

*--no-commit*
:   *pull*: merge without committing.

*--changed-only*
:   *download*, *pull*: only transfer files that changed locally as well.

*--no-verify*
:   Skip the *pre-ftp-push* hook.

*--no-post-hooks*
:   Skip the *post-ftp-push* hook.

*--enable-post-errors*
:   Fail when the *post-ftp-push* hook fails.

*--auto-init*
:   *push*: behave like *init* when the server has no log yet.

*--worktree*
:   Read the files to upload from a temporary Git worktree checked out at the
    commit being deployed, so edits to the working tree during the upload are
    ignored.

*--version*
:   Print the version and exit.

*-h*, *--help*
:   Print the help and exit.

## URL

The URL has the form *protocol://host.domain.tld:port/path*. Supported
protocols are *ftp://* (the default when none is given), *ftpes://* (explicit
TLS), *ftps://* (implicit TLS) and *sftp://*. *host:port/path* without a
protocol is accepted as FTP. Credentials may be given as
*ftp://user:password@host/path*; the password never appears in any output.

For SFTP, *sftp://host/dir* is relative to the login directory,
*sftp://host/~/dir* to the home directory and *sftp://host//dir* is absolute.

## DEFAULTS

Every option can be stored in the Git configuration:

    git config git-ftp.url ftp://example.com/public_html
    git config git-ftp.user alice
    git config git-ftp.password s3cret
    git config git-ftp.password-command "pass show example.com/ftp"
    git config git-ftp.syncroot public_html
    git config git-ftp.remote-root htdocs
    git config git-ftp.cacert /etc/ssl/certs/ca.pem
    git config git-ftp.insecure true
    git config git-ftp.disable-epsv true
    git config git-ftp.proxy http://proxy:3128
    git config git-ftp.key ~/.ssh/id_ed25519
    git config git-ftp.pubkey ~/.ssh/id_ed25519.pub
    git config git-ftp.key-passphrase ...
    git config git-ftp.keychain alice@example.com
    git config git-ftp.branch main
    git config git-ftp.no-commit true
    git config git-ftp.deployedsha1file .git-ftp.log
    git config git-ftp.jobs 8
    git config git-ftp.worktree true

The same keys may be placed in a *.git-ftp-config* file in the repository,
which takes precedence over the Git configuration.

## ENVIRONMENT

*GIT_FTP_URL*, *GIT_FTP_USER*, *GIT_FTP_PASSWORD*
:   Read after the command line and before the Git configuration.

*NETRC*
:   Alternative *~/.netrc* file. The netrc file is consulted only when neither
    a user nor a password was given by other means.

*SSH_AUTH_SOCK*
:   A running ssh-agent is used for SFTP authentication.

## SCOPES

Scopes hold a separate set of settings, for example for staging and
production:

    git config git-ftp.production.url ftp://live.example.com/htdocs
    git config git-ftp.production.password s3cret
    git ftp push -s production

Unset scope keys fall back to the plain keys. An explicitly empty scope value
masks the plain value. *git ftp push -s* uses the current branch name as the
scope name. *add-scope* and *remove-scope* manage scopes from the command line.

## IGNORING FILES

*.git-ftp-ignore* in the repository root lists shell glob patterns, one per
line, of Git paths that are never uploaded (and never deleted). As in the
original, *\** also matches */* and the pattern has to match the whole path:

    config/*
    *.txt
    foobar.txt
    .gitignore
    */.gitkeep
    .git-ftp-ignore
    .git-ftp-include

## SYNCING UNTRACKED FILES

*.git-ftp-include* uploads files that are not tracked by Git:

    !VERSION.txt
    css/style.css:scss/style.scss
    css/style.css:scss/mixins.scss
    vendor/:composer.lock
    dist/style.css:/src/style.scss

A line starting with *!* always uploads the file. *target:source* uploads
*target* whenever the tracked *source* changed since the deployed commit. With
*--syncroot* the source is relative to the syncroot unless it starts with */*.
A directory target uploads everything below it. A target that no longer exists
locally is deleted on the server. Ignore patterns still apply afterwards.

## PARALLEL TRANSFERS

Files are transferred over several connections at once (*--jobs*, default 4).
Uploads happen first, then deletes, then the log is written. The first failed
upload aborts the deploy with exit code 4 and the log is left untouched; a
failed delete is only a warning. Ctrl-C stops the transfers and exits with 130.

## WORKTREE

With *--worktree* (or *git config git-ftp.worktree true*) *init* and *push* check
the deployed commit out into a throwaway Git worktree and read the uploaded file
contents from there. Editing the working tree while a long upload is running then
cannot change what is deployed. The worktree shares the object store, so only a
working copy is written to disk; it is removed when the deploy finishes. Untracked
files added through *.git-ftp-include* are not part of the commit and are read from
the live working tree as before.

## LOCKING

With *--lock* a file *git-ftp.lck* containing the commit id and the user is
written on the server before the transfer and removed afterwards. A deploy of
a different commit refuses to run while the lock exists (exit code 7); *--force*
ignores the lock and *unlock* removes it.

## DOWNLOADING

*download*, *pull* and *snapshot* list the remote directory (MLSD, falling back
to LIST) and download files that are missing locally or differ in size or
modification time. Files missing on the server are deleted locally unless they
are ignored, part of *.git* or one of git-ftp's own files.

## HOOKS

*pre-ftp-push* and *post-ftp-push* in the repository's hooks directory
(*core.hooksPath* is honoured) are run with four arguments: the scope name or
host, the display URL, the local commit and the deployed commit (the previous
one for the post hook). The pre hook receives the NUL separated change list
(*A path* / *D path*) on stdin; a non-zero exit aborts the deploy with exit code
9. The post hook's exit status is ignored unless *--enable-post-errors* is
given.

## SFTP HOST KEYS

Host keys are verified against *~/.ssh/known_hosts* and
*/etc/ssh/ssh_known_hosts*. Add a server with

    ssh-keyscan -p 22 host >> ~/.ssh/known_hosts

or pass *--insecure* to skip the verification.

## EXIT CODES

0
:   success

1
:   unexpected error

2
:   wrong usage

3
:   missing argument

4
:   error while uploading (also: remote not reachable, login failed)

5
:   error while downloading (also: *push* before *init*)

6
:   unknown protocol

7
:   remote locked

8
:   not a Git project, dirty working tree or invalid branch

9
:   hook failed

10
:   local filesystem error

130
:   interrupted

## SEE ALSO

git(1), curl(1). Upstream: <https://github.com/git-ftp/git-ftp>
