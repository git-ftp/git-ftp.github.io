---
title: Scopes
---

# Scopes

A scope is a named set of settings in the same repository — one for staging,
one for production, one for a customer's server.

## Creating a scope

The `add-scope` action takes everything from a URL:

```sh
git ftp add-scope production ftp://alice:s3cret@live.example.com/htdocs
git ftp add-scope staging    ftp://alice:s3cret@staging.example.com/htdocs
```

Or set the keys yourself:

```sh
git config git-ftp.production.url  "ftp://live.example.com/htdocs"
git config git-ftp.production.user "manager"
git config git-ftp.production.password "n0tThatSimp3l"
```

## Deploying to a scope

```sh
git ftp push -s production
git ftp init -s staging
```

Keys the scope does not define fall back to the plain `git-ftp.*` keys, so
shared settings are written once:

```sh
git config git-ftp.user alice                    # used by every scope
git config git-ftp.staging.url ftp://staging.example.com/htdocs
```

An explicitly empty scope value masks the plain value:

```sh
git config git-ftp.staging.syncroot ""           # no syncroot for staging
```

## The branch as the scope

If a scope is named after a branch, `-s` without a value uses the current
branch's name:

```sh
git checkout production
git ftp push -s          # pushes to the "production" scope
```

That makes a deploy step in CI identical for every environment.

## Removing a scope

```sh
git ftp remove-scope staging
```

!!! warning "Scopes hold credentials"

    `add-scope` writes the password from the URL into `.git/config`. That file
    is not committed, but it is readable by anyone with access to your
    checkout. On shared machines and in CI, prefer
    [other ways of passing a password](protocols.md#credentials).
