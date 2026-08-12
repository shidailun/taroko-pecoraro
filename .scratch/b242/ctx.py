# -*- coding: utf-8 -*-
import io,json,os,re,sys,collections
sys.stdout.reconfigure(encoding="utf-8")
H=os.path.abspath("."); SITE=os.path.join(H,"site"); ORTH=os.path.join(H,"tools","orthography")
read=lambda p: io.open(p,encoding="utf-8").read()
s=read(os.path.join(SITE,"entries.js")); ENT=json.loads(s[s.index("["):s.rindex("]")+1])
def wordKey(w): return re.sub(r"[’ʼ\"ʔ]","'",(w or "").lower()).replace("ł","l")
TOK=re.compile(r"[A-Za-zÀ-ÿł'’ʼ\"]+")
USES=collections.defaultdict(list)
for e in ENT:
    def walk(o,parent):
        for x in (o.get("examples") or []):
            t=x.get("t") or ""
            for tk in set(wordKey(z) for z in TOK.findall(t)):
                USES[tk].append((parent,t,x.get("zh") or ""))
    walk(e,e.get("hw"))
    for sb in (e.get("subs") or []): walk(sb,(e.get("hw") or "")+" / "+(sb.get("form") or ""))
ANS=json.load(io.open(".scratch/b242/answers.json",encoding="utf-8"))
out=[]
for it in ANS:
    k=wordKey(it["raw"])
    rows=USES.get(k) or []
    out.append("%02d %s  A=%s   (%d sentences)"%(it["n"],it["raw"],it["ans"],len(rows)))
    seen=set()
    for p,t,z in rows:
        if t in seen: continue
        seen.add(t)
        out.append("    [%s] %s"%(p,t))
        out.append("       中 %s"%z)
io.open(".scratch/b242/ctx.txt","w",encoding="utf-8").write("\n".join(out))
print(len(out))
