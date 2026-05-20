# LUMINA Standard

This repository contains the source files for the public LUMINA Standard website.

**Public site:** https://lumina.sabercraft.org/  
**Founding school/community:** https://sabercraft.org/

## What is LUMINA?

LUMINA is a lightsaber choreography standard for recording, teaching, sharing, and safely performing choreographed saber combat.

It is developed and maintained by **Lumina Federation LLC** and originated through the **SaberCraft** community.

## Repository purpose

This repo is intended to hold:

- official Markdown documentation
- versioned standard content
- notation references
- movement library structure
- downloadable release files
- changelog and governance materials

## Local preview

Install dependencies:

```bash
pip install -r requirements.txt
```

Run locally:

```bash
mkdocs serve
```

Build:

```bash
mkdocs build
```

## Publishing

This repo includes a GitHub Actions workflow that can publish the site to GitHub Pages.

Before publishing, confirm:

- `repo_url` in `mkdocs.yml`
- `repo_name` in `mkdocs.yml`
- `docs/CNAME` points to `lumina.sabercraft.org`
