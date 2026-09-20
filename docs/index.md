---
title: Upload to FTP servers the Git way
---

# Git-ftp

**Upload to FTP servers the Git way.**

If you use Git and you need to get your files onto an FTP server, Git-ftp saves
you time and bandwidth by uploading only the files that changed since the last
upload.

It records the deployed commit in a log file on the server and uses Git to work
out which local files differ from it. Nothing has to be installed on the server,
and you can just as well deploy another branch or go back in history to upload
an older version.

<div class="grid cards" markdown>

-   :material-download: **Install**

    ---

    `pip install git-ftp`, a package from your distribution, or a single shell
    script.

    [:octicons-arrow-right-24: Installation](getting-started/install.md)

-   :material-rocket-launch-outline: **First deployment**

    ---

    From an empty server to `git ftp push` in five commands.

    [:octicons-arrow-right-24: Get started](getting-started/first-deployment.md)

-   :material-cog-outline: **Configuration**

    ---

    Store the URL, the user and the password once, then deploy with a single
    command.

    [:octicons-arrow-right-24: Configuration](guide/configuration.md)

-   :material-book-open-variant: **Manual**

    ---

    Every action, option and configuration key of both implementations.

    [:octicons-arrow-right-24: Reference](reference/manual-python.md)

</div>

## In a nutshell

=== "Python"

    ```sh
    # Install
    pip install git-ftp

    # Setup
    git config git-ftp.url "ftp://ftp.example.net:21/public_html"
    git config git-ftp.user "ftp-user"
    git config git-ftp.password "secr3t"

    # Upload all files
    git ftp init

    # Or, if the files are already on the server
    git ftp catchup

    # Work and deploy
    echo "new content" >> index.txt
    git commit index.txt -m "Add new content"
    git ftp push
    # 1 file to sync:
    # [1 of 1] Buffered for upload 'index.txt'.
    # Uploading ...
    # Last deployment changed from 1f2a3b4 to ded01b27e5c785fb251150805308d3d0f8117387.
    ```

=== "Bash"

    ```sh
    # Setup
    git config git-ftp.url "ftp://ftp.example.net:21/public_html"
    git config git-ftp.user "ftp-user"
    git config git-ftp.password "secr3t"

    # Upload all files
    git ftp init

    # Or, if the files are already on the server
    git ftp catchup

    # Work and deploy
    echo "new content" >> index.txt
    git commit index.txt -m "Add new content"
    git ftp push
    # 1 file to sync:
    # [1 of 1] Buffered for upload 'index.txt'.
    # Uploading ...
    # Last deployment changed to ded01b27e5c785fb251150805308d3d0f8117387.
    ```

If something goes wrong, add `-v` or `-vv` to see what happens on the wire.

## Two implementations, one deployment

There are two git-ftp programs, and this site documents both.

| | [git-ftp][py] (Python) | [git-ftp][sh] (Bash) |
|---|---|---|
| Install | `pip install git-ftp` | package manager, or one shell script |
| Needs | Python 3.10+, `git` | `curl`, `git`, a POSIX shell |
| Protocols | FTP, FTPS, FTPES, SFTP | FTP, FTPS, FTPES, SFTP |
| Transfers | parallel (`--jobs`, default 4) | sequential |
| `download` / `pull` / `snapshot` | built in | needs `lftp` |
| Status | actively developed | the classic, in most distributions |

They read the same configuration, write the same `.git-ftp.log` and honour the
same `.git-ftp-ignore` and `.git-ftp-include` files, so a deployment made with
one can be continued with the other.

[:octicons-arrow-right-24: Which one should I use?](getting-started/implementations.md)

## Limitations

- **git-ftp is not a centralised deployment tool.** While a commit is being
  uploaded, the files belonging to it must stay untouched — no commits, no
  checkouts, no edits — or the uploaded contents will not match the commit.
  The Python implementation can take that worry away with
  [`--worktree`](guide/configuration.md#consistent-uploads-while-editing).
- **Windows and macOS are lightly tested**, especially for the Bash version.
  Bug reports and fixes for those platforms are very welcome.

[py]: https://github.com/git-ftp/git-ftp-py
[sh]: https://github.com/git-ftp/git-ftp
