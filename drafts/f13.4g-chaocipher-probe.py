import ctypes, random, sys, time
sys.path.insert(0,'/Users/alexisrondeau/Workshop/cryptos')
L=ctypes.CDLL('/tmp/chao/c.so'); L.icstream.restype=ctypes.c_double; L.anneal.restype=ctypes.c_double
L.anneal.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_long,ctypes.c_double,ctypes.c_uint64,ctypes.c_void_p]
A="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
def chao(pt,left,right):
    left,right,out=list(left),list(right),[]
    for p in pt:
        i=right.index(p); out.append(left[i])
        left=left[i:]+left[:i]; x=left.pop(1); left.insert(13,x)
        right=right[i:]+right[:i]; right=right[1:]+right[:1]; x=right.pop(2); right.insert(13,x)
    return "".join(out)
src=open('/Users/alexisrondeau/Workshop/cryptos/knowledge/sources/carter-1923-tomb-of-tutankhamen-vol1.txt',errors='ignore').read().upper()
src="".join(c for c in src if c.isalpha())
rng=random.Random(5)
for k in range(3):
    o=rng.randrange(len(src)-97); pt=src[o:o+97]
    l=list(A); rng.shuffle(l); r=list(A); rng.shuffle(r)
    ct=chao(pt,l,r); cti=(ctypes.c_int*97)(*[A.index(c) for c in ct])
    L0=(ctypes.c_int*26)(*[A.index(c) for c in l])
    tru=L.icstream(L0,cti,97,None)
    rnds=[]
    for _ in range(20000):
        q=list(range(26)); rng.shuffle(q); rnds.append(L.icstream((ctypes.c_int*26)(*q),cti,97,None))
    t=time.time(); best=(ctypes.c_int*26)()
    bs=max(L.anneal(cti,97,2_000_000,0.004,s,best) for s in range(3))
    print(f"true IC {tru:.4f}  random max of 20k {max(rnds):.4f} mean {sum(rnds)/len(rnds):.4f}  annealed best {bs:.4f}  match {list(best)==[A.index(c) for c in l]} {time.time()-t:.0f}s")
