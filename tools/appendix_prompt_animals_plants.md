# Appendix 2+3 — animal and plant names (pages 393-395), transcription-only

Two-column glossed word lists. Page 393 begins with the heading "QUELQUES NOMS
D'ANIMAUX" (animal names); somewhere in this range it switches to plant names
(look for a heading like "QUELQUES NOMS DE PLANTES" or similar — note it in your
final message if the exact page isn't obvious). Each line is a Truku name
followed by `=` and its French gloss (the animal or plant species).

Read these page images IN ORDER: {FILES}

## Rules
- Preserve the Truku spelling exactly as printed.
- Transcribe the French gloss faithfully (species name); rejoin typewriter
  line-break hyphenation.
- Do NOT translate to English or Chinese — a later pass adds that from the French.
- Read BOTH columns of each page, left column top-to-bottom then right column.
- If illegible, best reading + `(?)`. Never skip a line.
- Tag each entry `"animal"` or `"plant"` depending on which section it's in.

## Output
Write ONE file with the Write tool to: {OUT}
JSON, UTF-8:

```json
{
  "pages": [393, 395],
  "leadin": null,
  "entries": [
    { "hw": "...", "tag": "animal", "fr": "...", "examples": [], "subs": [] },
    { "hw": "...", "tag": "plant", "fr": "...", "examples": [], "subs": [] }
  ]
}
```

- `entries`: every name on your pages, in printed order (column order as read above).
- `leadin`: null unless the top of your first page continues an entry cut off from
  the previous page — if so, `{ "fr": "..." }` completing it.

Final message: one line only — number of entries written, where the animals→plants
section break falls (page + line), and any problem pages.
