# Migration sources

Source material for porting the Extended Library CM lessons from sabercraft.org
into `docs/core/`. One JSON file per CM, plus the script that produced them.

This directory sits outside `docs/`, so nothing here is published to
https://standard.sabercraft.org. It exists only to feed the migration.

## Why the files are here at all

The migration is run by a scheduled cloud agent, and that environment has no
outbound web access — every request to sabercraft.org is refused at the egress
proxy. Fetching the lessons at migration time is therefore impossible. These
files are the lessons captured ahead of time, from a machine that can reach the
site, so the migration can read them from disk instead.

## What each file holds

| Field | Meaning |
|---|---|
| `cm`, `focus`, `source_url` | Which CM this is, and the lesson it came from |
| `page_title` | The source page's `<title>` |
| `youtube_id` | The lesson video, for the page's embed. `null` when the lesson has no video |
| `prose` | The lesson's own paragraphs — intro, contributor credit |
| `body_text` | The entire post body as plain text. Some lessons write their notation in running text rather than in a table, so this is the fallback that catches everything |
| `tables` | One entry per notation table: its caption (which is where the telegraph lives), and its rows |
| `warnings` | Anything missing or unusual about this capture |
| `access` | Present, and set to `login_required`, when the lesson is behind a member login |

Two kinds of table appear across these lessons and both are captured:
`nt_type_ajax_table` ships an empty `<table>` and serves its rows from
`admin-ajax.php`, while `nt_type_legacy_table` renders its rows inline in the
page HTML. The `kind` field on each table records which one it was.

## Known gaps

- **CM-U is behind a member login.** `choreography-kvr/` returns the "seems like
  you haven't logged in yet" page to anonymous requests, so there is no source
  material for it here and none can be captured this way. It needs to be
  supplied by hand.
- **CM-G has no video** on its lesson page.
- **CM-I and CM-J have no notation table.** Their sequences are written as
  running text in the page body, so read `body_text` for those two.
- CM-K and CM-L share a video; they are two parts of the same filmed fight.

## Regenerating

    python migration-sources/fetch-sources.py

Run from the repo root, from a machine with web access. It reads the CM list and
lesson URLs straight out of `docs/core/extended-library.md`, so it only fetches
rows that have not been migrated yet — a migrated row no longer carries a
sabercraft.org link. Pass CM letters to limit it:

    python migration-sources/fetch-sources.py CM-K CM-L

Once every row is migrated this directory can be deleted.
