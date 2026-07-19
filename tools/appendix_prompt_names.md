# Appendix 4 — personal names (pages 396-398), transcription-only

Structurally different from the rest of the dictionary: bare multi-column name
lists, no French gloss per name. Page 396 opens with a "REMARQUE" prose note
(explaining naming conventions), then "NOMS plus souvent portés par des FEMMES"
(women's names), then a men's names section (heading may read something like
"NOMS ... HOMMES" or just continue after the women's list — note where the
split falls). A `+` prefix on a name marks Japanese-origin. The dictionary and
colophon ("Paris 128 R. du Bac / Octobre 1976 - Juin 1977") end on page 398.

Read these page images IN ORDER: {FILES}

## Rules
- Preserve spelling exactly as printed.
- Read ALL columns of each page, left to right, top to bottom within each column.
- A name prefixed `+` is Japanese-origin — encode this in `tag`.
- Do NOT translate anything to English or Chinese.
- If illegible, best reading + `(?)`. Never skip a name.
- Transcribe the REMARQUE prose verbatim as its own entry (hw: "REMARQUE",
  tag: "note", fr: the French prose text).
- Transcribe the closing colophon verbatim too (hw: "COLOPHON", tag: "note",
  fr: the colophon text) if it falls within your pages.

## Output
Write ONE file with the Write tool to: {OUT}
JSON, UTF-8:

```json
{
  "pages": [396, 398],
  "leadin": null,
  "entries": [
    { "hw": "REMARQUE", "tag": "note", "fr": "...", "examples": [], "subs": [] },
    { "hw": "...", "tag": "name (f)", "fr": "", "examples": [], "subs": [] },
    { "hw": "...", "tag": "name (f, jp)", "fr": "", "examples": [], "subs": [] },
    { "hw": "...", "tag": "name (m)", "fr": "", "examples": [], "subs": [] }
  ]
}
```

- `tag` values: `"name (f)"`, `"name (f, jp)"`, `"name (m)"`, `"name (m, jp)"`,
  or `"note"` for the REMARQUE/colophon entries.
- `entries`: every name on your pages, in printed reading order.
- `leadin`: null (names don't continue across the appendix boundary from 393-395).

Final message: one line only — number of names transcribed, where women's→men's
section splits, and any problem pages.
