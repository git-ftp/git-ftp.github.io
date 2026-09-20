---
title: Getting started
---

# Getting started

Three short pages get you from nothing to a deployed site:

<div class="grid cards" markdown>

-   :material-download: **[Install](install.md)**

    ---

    Pick an implementation and get `git ftp` onto your `PATH`.

-   :material-rocket-launch-outline: **[First deployment](first-deployment.md)**

    ---

    Configure a server, upload everything once, then push only what changed.

-   :material-scale-balance: **[Which implementation](implementations.md)**

    ---

    What the Python port and the Bash original do differently.

</div>

Everything after that is in the [guide](../guide/configuration.md), and every
option is listed in the [manuals](../reference/manual-python.md).

## What you need

- A Git repository whose files you want on a server.
- An account on that server, reachable over FTP, FTPS, FTPES or SFTP.
- Write permission in the directory you deploy into — git-ftp keeps its log
  file (`.git-ftp.log`) there.

Nothing is installed on the server, and the server needs no Git.
