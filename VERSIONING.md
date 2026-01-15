# Versioning Guide

This project manages versions using [Bump2Version](https://github.com/c4urself/bump2version).
The source of truth for the version is `main.py` (the `__version__` variable).

## Prerequisites

Ensure you have the requirements installed:

```bash
pip install -r requirements.txt
```

## How to Release a New Version

### 1. Update Release Notes
Before bumping the version, open `CHANGELOG.md` and:
1.  Move your changes from `[Unreleased]` to a new section for the new version (e.g., `## [1.1.8] - 2025-01-15`).
2.  Ensure the `[Unreleased]` section is empty and ready for future changes.

### 2. Bump the Version
Run one of the following commands in your terminal to bump the version, commit the change, and create a git tag:

**For a Bug Fix (1.1.7 -> 1.1.8):**
```bash
bumpversion patch
```

**For a New Feature (1.1.7 -> 1.2.0):**
```bash
bumpversion minor
```

**For a Breaking Change (1.1.7 -> 2.0.0):**
```bash
bumpversion major
```

**Note:** This command will automatically:
- Update `__version__` in `main.py`.
- Update `current_version` in `.bumpversion.cfg`.
- Create a git commit with the message `Bump version: x.x.x → y.y.y`.
- Create a git tag `vy.y.y`.

### 3. Push to Remote (GitHub)
To push the new commit AND the new tag to GitHub (which typically triggers your release workflow), run:

```bash
git push --follow-tags
```

## Automatic Build & Release
Once you push the tag, your GitHub Actions workflow (if configured) should:
1.  Detect the new tag (e.g., `v1.1.8`).
2.  Build the application/installer.
3.  Create a GitHub Release.

## Configuration
The configuration is found in `.bumpversion.cfg`.
