# Appendix 1 — loanwords (pages 390-392), transcription-only

Two-column glossed word list, e.g. `BIRU = Bière.` Each line is a Truku loanword
(often from Japanese or Chinese) followed by `=` and its French gloss.

Read these page images IN ORDER: {FILES}

## Rules
- Preserve the Truku spelling exactly as printed (headword = the word before `=`).
- Transcribe the French gloss faithfully; rejoin typewriter line-break hyphenation.
- Do NOT translate to English or Chinese — a later pass adds that from the French.
- Read BOTH columns of each page, left column top-to-bottom then right column.
- If illegible, best reading + `(?)`. Never skip a line.

## Output
Write ONE file with the Write tool to: {OUT}
JSON, UTF-8:

```json
{
  "pages": [390, 392],
  "leadin": null,
  "entries": [
    { "hw": "BIRU", "tag": "loanword", "fr": "Bière.", "examples": [], "subs": [] }
  ]
}
```

- `entries`: every loanword on your pages, in printed order (column order as read above).
- `leadin`: null unless the top of your first page continues a word cut off from the previous page (rare here since each line is self-contained) — if so, `{ "fr": "..." }` completing it.
- `tag` is always `"loanword"`.

Final message: one line only — number of entries written and any problem pages.
