# Batch transcription prompt template

Placeholders: {P1} {P2} = first/last PDF page number, {FILES} = image paths, {OUT} = output JSON path.

---

You are transcribing pages {P1}-{P2} of Ferdinando Pecoraro's *Essai de dictionnaire taroko-francais* (SECMI, Paris 1977) — a typewritten Truku (Taroko) -> French dictionary — from scanned page images, then translating the French glosses into English and Traditional Chinese (Taiwan).

Read these page images IN ORDER (one printed page each):
{FILES}

## Structure of the printed text
- Root headwords: CAPITALS at the left margin, double-underlined, often followed by (R) [= racine/root]. Example: `ADAS (R) = Apporter - emporter - prendre avec soi.`
- Derived sub-forms: indented, underlined, initial capital (Madas, Kndkilan, P'adas...). They belong to the preceding root entry.
- `°` introduces a verb paradigm list (e.g. `° Madas, adas, d'si, d'san, d'sun`).
- `§` introduces an example: Truku sentence, then `=`, then French gloss.
- `d°` = "ditto / same as above": keep it as printed in fr; render the meaning naturally in en ("verbal form of the preceding") and zh (「同上之動詞形」etc.).
- A `=` at the END of a typed line is typewriter hyphenation: rejoin the word (`em=` + `porté` -> `emporté`). Do not confuse with the `=` separating Truku from its gloss.
- Ignore page headers/footers and the page number in parentheses at the top.

## Critical rules
- Preserve Pecoraro's idiosyncratic orthography EXACTLY as printed (x, ö, ç, ", ' , o for u, etc.). Do NOT modernize to current Truku spelling. Truku text appears in headwords, paradigms, and example sentences (`t` fields).
- Transcribe the French faithfully; fix only line-break hyphenation.
- en = faithful English translation of the French; zh = Traditional Chinese (Taiwan usage), faithful and natural, full-width punctuation.
- Translate parenthetical notes too. Conventions: `vl.` -> en "var." / zh 「或:」; `nb.` -> en "n.b." / zh 「註:」.
- If a word is illegible, give your best reading followed by `(?)`. Never silently skip content.

## Output
Write ONE file with the Write tool to: {OUT}
JSON, UTF-8, this exact shape:

```json
{
  "pages": [{P1}, {P2}],
  "leadin": null,
  "entries": [
    {
      "hw": "ADAS", "tag": "(R)",
      "crossRef": "optional — for entries that only point to another headword",
      "paradigm": "optional — the ° list, verbatim",
      "fr": "...", "en": "...", "zh": "...",
      "examples": [ {"t": "Truku text", "fr": "...", "en": "...", "zh": "..."} ],
      "subs": [
        { "form": "Madas", "paradigm": "optional", "fr": "...", "en": "...", "zh": "...",
          "examples": [ {"t": "...", "fr": "...", "en": "...", "zh": "..."} ] }
      ],
      "truncated": true
    }
  ]
}
```

- `leadin`: if the TOP of page {P1} continues an entry begun on the previous page (text before the first root headword), put that continuation here as `{ "fr": "...", "en": "...", "zh": "...", "examples": [...], "subs": [...] }` — running text in fr/en/zh (empty strings if none), complete examples in `examples`, sub-forms (with their own examples) in `subs`. Otherwise `null`.
- `entries`: every root entry that STARTS on your pages, in printed order. Omit `crossRef`/`paradigm`/`truncated` when not applicable; `tag` is `""` when absent.
- Set `"truncated": true` ONLY on your last entry and only if the end of page {P2} cuts it off mid-entry.
- Be exhaustive: every entry, every sub-form, every example.

Final message: one line only — number of entries written and any problem pages.
