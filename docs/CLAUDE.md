# CLAUDE.md — SaberCraft Standard Repository

This repository is the canonical source for the **SaberCraft Standard**, a choreographed saber combat notation framework. It is published as an MkDocs Material site at https://standard.sabercraft.org. All documentation lives in `docs/`.

## Naming rules (strict — do not violate)

These terms were settled by formal architecture decisions. Never rename, "correct," or swap them:

- **SaberCraft Standard** — the framework itself. Formerly called "LUMINA Standard"; that rename is complete. Never reintroduce "LUMINA Standard."
- **LUMINA Games** — the optional game/scoring layer (Duels and Duets), documented under `docs/games/`. This keeps the LUMINA name permanently. Do not rename it to "SaberCraft Games."
- **Lumina Federation LLC** — the legal entity. Never alter, rebrand, or expand this name.
- **Saberist** — the general term for any practitioner of the SaberCraft Standard. Use this everywhere a practitioner is referenced.
- **Lumen / Lumens** — refers ONLY to players within LUMINA Games. Never use it as a general practitioner term.
- **CM** — short for **Choreography Movement**. Movements are identified by CM codes (CM-A, CM-B, ...). Overview pages use the public-facing heading "Core Movements." New students are directed to CM-A through CM-E first; the full catalog lives at https://sabercraft.org/cm-series-catalog/.
- **SaberCraft** (alone) — the founding school and community at https://sabercraft.org. When contrasting the framework with the school, write "the SaberCraft Standard" for the framework, never bare "SaberCraft." Pages such as `faq.md`, `for-schools.md`, `learn.md`, and `standard.md` deliberately contrast the two — do not "deduplicate" them.

## Technical exceptions

- CSS class names such as `lumina-hero`, `lumina-button`, and variables like `--lumina-red` are defined in `docs/assets/stylesheets/sabercraft.css` and are intentionally unchanged. Never rename them in markdown or CSS — doing so silently breaks homepage styling. A theme-wide class rename is a separate, deliberate future task tracked in Notion.
- `docs/CNAME` must contain exactly `standard.sabercraft.org`. Never change it as part of any other edit.

## Site and URL conventions

- Public site: https://standard.sabercraft.org (GitHub Pages, DNS via QUIC.cloud CNAME `standard` → `luminafederation.github.io`).
- https://sabercraft.org is the school/community site (WordPress) — a different property. Do not point framework doc links at it except where a page intentionally references the school (e.g., the CM catalog link above).
- The stale domain `lumina.sabercraft.org` is reserved for LUMINA Games. Do not use it in framework documentation.
- Diagrams for targets, attacks, and parries live in the repo as committed images. Attack and parry diagrams are laid out as 2×3 markdown tables with `{ width="200" }` thumbnails and bold inline captions; the three target-overview images are full-width figures. Preserve these layouts when editing those pages.

## Writing rules

- All pages under `docs/` are **student-facing**. No internal planning notes, steward commentary, TODO language, or "we will eventually" phrasing in published pages.
- Tone: clear, welcoming, instructional. Assume the reader is a new Saberist unless the page states otherwise.
- Do not invent mechanics, CM codes, terminology, or rules. If documentation is ambiguous or missing, stop and ask in the issue/PR rather than filling gaps.
- Licensing: the approved model is **CC BY-NC-SA** with a grassroots paid-teaching carve-out, plus a separate commercial license. Trademark, not copyright, is the primary guardrail. Do not restate licensing terms on other pages; link to `licensing.md`.

## Governance

- Newest approved documentation wins. Decisions are recorded in the project's Notion workspace; historical pages are bannered as superseded, not rewritten.
- Prefer small, reviewable commits. When a change touches naming, licensing, or structure, describe the rationale in the PR body.
