# The monospace grid — reading a character COUNT off the page

A technique, not a finding. Written up because it settles a class of question
that letterform inspection cannot settle at all.

## The method

Pecoraro's manuscript was typed on a fixed-pitch typewriter. At the resolution
the `scans/full/page_NNN.png` renders were made, **one character cell is ~16px
wide**. A word's ink extent therefore counts its characters:

```
cells ≈ ink_width / 16          (an n-character word spans ≈ 16n px)
```

Measure it by taking a horizontal band across the line's x-height, summing dark
pixels per column, and cutting the row into words at runs of ≥7 blank columns:

```python
row = numpy.array(Image.open(page).convert("L"))[y0:y1, :]
ink = (row < 128).sum(axis=0)
# then split on gaps of >= 7 blank columns
```

Always calibrate the pitch on the SAME line, against words whose spelling is not
in question. On page 164 the LIWANG example line gives `liwang` 101px / 6 chars,
`klaon` 83 / 5, `mo` 32 / 2, `na` 31 / 2 — a consistent ~16px cell — and the
word under examination measured 99px, i.e. **6 cells**, the same as `liwang`.

## Why it is worth having

**A character count is a hard constraint that is independent of letterform.**
Every other test we run on a suspected misreading — the shape of the glyph, the
family, the frequency, the gloss — is an argument about what the letters are.
This one is an argument about how many there are, and it can refuse a reading
outright without ever identifying a single letter.

That is exactly what is needed for the confusions this typeface produces. Its
`m` is a low, flat three-stem glyph whose left stem plus first arch reads
convincingly as `r`, and the scans carry ink specks that supply a phantom
`i`-dot. So `mnalox` (6 cells) was transcribed `rinalox` (7 characters). No
amount of staring at the glyph resolves that; the cell count does, immediately.

## The trap: the confusion runs BOTH directions on the same line

This cannot be swept as a rule. On page 164 the single line
`§ Pax liwang nia ka klaon mo mnalox na` contains one `m` that WAS misread as
`ri`, and another `m` — in `mo` — that was transcribed correctly although the
page appears to read `no`. Page 165 has the typewriter setting French `maigre`,
`maigreur`, `moi`, `mes` in shapes that read as `naigre`, `naigreur`, `noi`,
`nes`.

So a blanket `n→m` or `ri→m` sweep would corrupt as much as it fixed. **The grid
is a per-word adjudication tool.** It answers "how many characters are in THIS
word", one word at a time, against a pitch calibrated on THAT line.

## Order of operations

Unchanged from the standing rule: propose the "it's his" reading first. The grid
is what refuses it when it deserves refusing. For `rinalox` the corpus refused it
too — one occurrence in 398 pages against `mnalox` ×152, `sknalox` ×56, `nalox`
×14, and no r-initial member anywhere in the family — but the corpus argument is
circumstantial and the grid argument is not.

## What it opens

The candidate shape is: **a type occurring exactly once in all 398 pages while a
near-neighbour one character away occurs many times.** That is the `rinalox` /
`mnalox` signature. It is a candidate list for grid checks, never a fix list —
see `.claude/notes/batch-log.md` for the measurement and for `manalox`, which
wears the same shape and has not been checked against its page yet.
