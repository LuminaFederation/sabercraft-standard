# The Saber Standard

This repository contains the source files for the public SaberCraft Standard website.

**Public site:** <https://standard.sabercraft.org/>
**Founding school/community:** <https://sabercraft.org/>

## What is the SaberCraft Standard?

The SaberCraft Standard is a choreography standard for recording, teaching, sharing, and safely performing choreographed saber combat. It defines a shared movement notation, a controlled vocabulary, a Core Movement (CM) library structure, and a beginner learning path that schools, clubs, and individual Saberists can adopt.

It is maintained by **Lumina Federation LLC** and originated through the **SaberCraft** community.

## Repository purpose

This repo holds:

- official Markdown documentation (`docs/`)
- versioned standard content
- notation references
- movement library structure
- downloadable release files
- changelog and governance materials

The site is built with [MkDocs](https://www.mkdocs.org/) and published via GitHub Pages.

## Local preview

Install dependencies:

```
pip install -r requirements.txt
```

Run locally:

```
mkdocs serve
```

Build:

```
mkdocs build
```

## Publishing

This repo includes a GitHub Actions workflow that publishes the site to GitHub Pages.

Before publishing, confirm:

- `repo_url` and `repo_name` in `mkdocs.yml` reference `LuminaFederation/sabercraft-standard`
- `docs/CNAME` contains `standard.sabercraft.org`

## Contributing

See [Contributing and Submissions](https://standard.sabercraft.org/contributing-and-submissions/) on the public site for how movements and notation proposals are reviewed, and `CLAUDE.md` for repository conventions.

## License

The SaberCraft Standard is published under the licensing terms described at [Licensing and Use Policy](https://standard.sabercraft.org/licensing/).
