---
title: Install
---

# Install

=== "Python (recommended)"

    The Python implementation is published on
    [PyPI](https://pypi.org/project/git-ftp/) and needs Python 3.10 or newer.

    ```sh
    pip install git-ftp
    ```

    Prefer an isolated installation, so the tool does not share a virtual
    environment with anything else:

    ```sh
    pipx install git-ftp     # or
    uv tool install git-ftp
    ```

    Check it:

    ```sh
    git ftp --version
    ```

    Git runs the `git-ftp` program as `git ftp` as soon as it is on your
    `PATH`. libcurl comes bundled with the `pycurl` wheel and SFTP is spoken by
    `paramiko`, so the only other thing you need is `git` itself.

    Upgrade with `pip install --upgrade git-ftp` (`pipx upgrade git-ftp`,
    `uv tool upgrade git-ftp`).

=== "Bash"

    The original is a single shell script that needs `git` and `curl`.

    **Debian, Ubuntu and friends**

    ```sh
    sudo apt-get install git-ftp
    ```

    The distribution package can lag behind. For the newest release maintained
    by the project, add the PPA:

    ```sh
    sudo -s
    add-apt-repository ppa:git-ftp/ppa

    # On Debian, point the PPA at the precise series
    source /etc/*-release
    if [ "$ID" = "debian" ]; then
        dist="$(echo /etc/apt/sources.list.d/git-ftp-ppa-*.list | sed 's/^.*ppa-\(.*\)\.list$/\1/')"
        sed -i.backup "s/$dist/precise/g" /etc/apt/sources.list.d/git-ftp-ppa-*.list
    fi

    apt-get update
    apt-get install git-ftp
    ```

    **macOS**

    ```sh
    brew install git git-ftp
    ```

    **Arch Linux**

    Unofficial packages are in the
    [AUR](https://aur.archlinux.org/packages?K=git-ftp).

    **From source, any Unix**

    ```sh
    git clone https://github.com/git-ftp/git-ftp.git
    cd git-ftp

    # check out the newest release tag
    git checkout "$(git tag | grep '^[0-9]*\.[0-9]*\.[0-9]*$' | tail -1)"
    sudo make install
    ```

    To update, `git fetch`, check out the new tag and run `sudo make install`
    again.

    **The script alone**

    ```sh
    curl https://raw.githubusercontent.com/git-ftp/git-ftp/master/git-ftp > /bin/git-ftp
    chmod 755 /bin/git-ftp
    ```

    This installs the current development state. Replace `master` with a
    version tag to pin a release. Uninstall by deleting the file.

## Windows

=== "Python"

    Install Python from [python.org](https://www.python.org/downloads/) or the
    Microsoft Store, then:

    ```powershell
    pip install git-ftp
    git ftp --version
    ```

    All four protocols work out of the box; there is no separate curl to
    install.


    ## Shell completion

    The Python implementation ships completions:

    ```sh
    eval "$(_GIT_FTP_COMPLETE=bash_source git-ftp)"   # zsh: zsh_source, fish: fish_source
    ```

    Add the line to your shell's startup file to keep it.

=== "Bash"

    Install [Git for Windows](https://gitforwindows.org/), open Git Bash as
    administrator and run:

    ```bash
    curl https://raw.githubusercontent.com/git-ftp/git-ftp/master/git-ftp > /bin/git-ftp
    chmod 755 /bin/git-ftp
    ```

    `/bin` here is an alias, by default `C:\Program Files\Git\usr\bin`.

    For SFTP you need a [curl build](https://curl.se/windows/) with SFTP
    support: install it and remove `bin/curl.exe` from the Git for Windows
    directory so the new one is found.

    Cygwin works too — install its `curl` package and use the same two
    commands.

    ??? warning "Git for Windows and Cygwin side by side"

        If both are installed you may see an error about a path starting with
        `/cygdrive/`:

            creating `/cygdrive/c/TEMP/git-ftp-m7GH/delete_tmp': No such file or directory

        git-ftp then mixes commands from both installations, which disagree on
        path prefixes. Edit `<cygwin>\etc\fstab` and change

            none /cygdrive/ cygdrive binary,posix=0,user 0 0

        to

            none / cygdrive binary,posix=0,user 0 0

        Close all consoles and try again.

    ## SFTP on macOS with the Bash version

    The curl that ships with macOS has no SFTP support and reports
    `Protocol sftp not supported or disabled in libcurl`. Either use the
    [Python implementation](implementations.md), which speaks SFTP through paramiko, or
    build curl yourself:

    ```sh
    # in the unpacked curl source from https://curl.se/download.html
    brew install openssl libssh2
    ./configure -q --with-libssh2 --with-ssl=/usr/local/opt/openssl
    make
    make install
    ```

    `curl --version` should then list `sftp` among the protocols. If the system
    curl still wins, put `/usr/local/bin` first in your `PATH`.
