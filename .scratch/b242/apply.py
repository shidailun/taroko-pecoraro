# -*- coding: utf-8 -*-
import json, io, collections

P = 'tools/orthography/manual_map.json'
m = json.load(open(P, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)

CHANGES = {
  # --- the itch root: his QLAQ family is modern rkrak ---
  "mqlaq":       "mrkrak",
  "qlaq":        "rkrak",
  "sqlaq":       "srkrak",
  "q'loq":       "rkruk",
  # --- the weaving shuttle ---
  "ksudan":      "kusutan",
  # --- the gluttony root: bsiyak, not the basiq tree ---
  "tibasyaq":    "tbsiyak",
  "tbasyaq":     "tbsiyak",
  "dmbasyaq":    "dmbsiyak",
  "dmt'basyaq":  "dmptbsiyak",
  # --- the covering root ---
  "xlakux":      "hlakuk",
  "mpxlakux":    "emphlakuk",
  # --- rust ---
  "mslangan":    "skringan",
  "mpslangan":   "empskringan",
  # --- seize ---
  "glaqon":      "glkun",
  # --- jealousy: the -an slot of sneuhir ---
  "snxelan":     "snhiran",
  # --- leftover: the -an slot batch 220 left inferred ---
  "lngiyan":     "rngian",
  "pnslngiyan":  "pnsrngian",
  # --- singles ---
  "ulang":       "ulan",
  "sloweq":      "sruwaq",
  "qlap":        "qrak",
  "sxmqan":      "shmuk",
  "sm":          "smdalih",
  "sm'mul":      "seemur",
  "sn'mul":      "sneemur",
  "mngusyex":    "mngasih",
}

before = {k: m.get(k, None) for k in CHANGES}
m.update(CHANGES)
out = collections.OrderedDict(sorted(m.items(), key=lambda kv: kv[0]))
with io.open(P, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
    f.write('\n')

for k, v in CHANGES.items():
    print('%-14s %-14s -> %s' % (k, before[k] if before[k] is not None else '(absent)', v))
print('keys %d -> %d' % (len(before) and len(json.load(open(P,encoding='utf-8'))), len(out)))
