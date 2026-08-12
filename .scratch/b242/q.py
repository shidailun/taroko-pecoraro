# -*- coding: utf-8 -*-
import io,json,os,re,sys,collections,difflib
sys.stdout.reconfigure(encoding="utf-8")
ORTH=os.path.join(os.path.abspath("."),"tools","orthography")
J=lambda n: json.load(io.open(os.path.join(ORTH,n),encoding="utf-8"))
GL=[J("attested_gloss.json"),J("bible_gloss.json"),J("parquet_gloss.json")]
LEX=set(J("attested_modern.json"))
def gl(w):
    o=[]
    for D in GL:
        g=D.get(w) or []
        for x in (g if isinstance(g,list) else [g]):
            x=str(x).strip()
            if x and x not in o: o.append(x)
    return o
def ed(a,b):
    if abs(len(a)-len(b))>3: return 9
    p=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        c=[i]
        for j,cb in enumerate(b,1):
            c.append(min(p[j]+1,c[j-1]+1,p[j-1]+(ca!=cb)))
        p=c
    return p[-1]
mode=sys.argv[1]
args=sys.argv[2:]
if mode=="w":
    for w in args:
        print("== %s  %s  %s"%(w,"LISTED" if w in LEX else "not-listed"," / ".join(gl(w))[:120]))
        near=sorted(((ed(w,x),x) for x in LEX if abs(len(x)-len(w))<=2),key=lambda t:(t[0],t[1]))[:12]
        for d,x in near:
            if d<=2: print("   ~%d %-14s %s"%(d,x," / ".join(gl(x))[:80]))
elif mode=="z":
    # find register words whose gloss contains any of the chars, with carrier counts
    cnt=collections.Counter()
    for D in GL:
        for k,v in D.items():
            for x in (v if isinstance(v,list) else [v]):
                for c in set(re.findall(r"[㐀-鿿]",str(x))): cnt[c]+=1
    for ch in args:
        hits=set()
        for D in GL:
            for k,v in D.items():
                for x in (v if isinstance(v,list) else [v]):
                    if ch in str(x): hits.add(k)
        print("== %s  carriers=%d  words=%d"%(ch,cnt[ch],len(hits)))
        for w in sorted(hits)[:60]: print("   %-16s %s"%(w," / ".join(gl(w))[:70]))
elif mode=="p":  # prefix/substring search in LEX
    for a in args:
        hits=sorted(w for w in LEX if a in w)
        print("== *%s*  %d"%(a,len(hits)))
        for w in hits[:40]: print("   %-16s %s"%(w," / ".join(gl(w))[:70]))
