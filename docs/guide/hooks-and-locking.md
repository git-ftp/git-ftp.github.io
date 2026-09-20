---
title: Hooks and locking
---

# Hooks and locking

## Hooks

git-ftp runs two client-side hooks during `init` and `push`, from the
repository's hooks directory (`.git/hooks`, or `core.hooksPath` if set).

`pre-ftp-push`
:   Runs after the list of changed files has been built, just before the first
    upload. A non-zero exit aborts the deployment with exit code 9. Skipped
    with `--no-verify`.

`post-ftp-push`
:   Runs after the transfer finished. Its exit status is ignored unless
    `--enable-post-errors` is given. The Python implementation can skip it with
    `--no-post-hooks`.

Both receive four arguments:

| | |
|---|---|
| `$1` | the scope name, or the host if no scope is used |
| `$2` | the URL being deployed to |
| `$3` | the local commit being uploaded |
| `$4` | the commit currently recorded on the server |

`pre-ftp-push` additionally gets the change list on standard input: `A ` or
`D ` followed by the path, entries separated by NUL bytes. `A` means the file
is scheduled for upload, `D` for deletion. This list is not the same as
`git diff` — `.git-ftp-include` and `.git-ftp-ignore` have already been applied
to it, and it contains the syncroot if one is set.

### An example

`.git/hooks/pre-ftp-push`, executable, refusing to deploy a file that still
contains `TODO`:

```bash
#!/bin/bash
#
# $1 -- scope name or host   $3 -- local commit
# $2 -- URL                  $4 -- commit on the server
#
# stdin: NUL separated "<A|D> <path>" entries

while read -r -d '' status file
do
    if [ "$status" = "A" ]; then
        if grep -q 'TODO' "$file"; then
            echo "TODO found in $file, not uploading."
            exit 1
        fi
    fi
done

exit 0
```

Typical uses: building assets, clearing a cache through an HTTP call, posting a
deployment notice to chat, or refusing to deploy anything but a release tag.

!!! note "Experimental in the Bash implementation"

    The interface may still change there. The Python implementation runs the
    same hooks with the same arguments.

## Locking

Two deployments running at once would fight over the same files. `--lock`
prevents that:

```sh
git ftp push --lock
```

Before the transfer, git-ftp writes `git-ftp.lck` on the server containing the
commit id and the user. While it exists, a deployment of a *different* commit
refuses to run and exits with code 7. A deployment of the same commit is
treated as your own and proceeds. The file is removed when the deployment
finishes.

If a deployment was interrupted and left the lock behind:

```sh
git ftp unlock          # Python implementation
git ftp push --force    # ignore the lock and deploy anyway
```
