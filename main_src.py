import base64
TB=base64.b85decode("AP9mW2!gP!!fRc6Ur3f}N^+eTj-)7Z+xLlL7;@Y9c_3JN8pv@SX>uS4f*=TjM5JLV)Hzhfnxq<bm};tS&7Ph(qO6RXm`IxJYl@X9j;ASd6G?vLSY|-zhM#0f8z^a97J8f5d8ImHoq3ujYJML$qNW*spD2>07=oZEiXu6NpeTajSc2Nuah{iP<yoR?Se|5=s_jai-$<I`sfwHzlBDTz+U9|w7jhWabs+d@SjTyw_)(k(iejj38%T=kIdk3id7tNf9Vmif_=Q~<f?x=O9{7P_2!7oce&F|coX34$_jMi^f?()%6)AR>28txedES?89tn0_IC9+>c4Sv}9$1Rx=#8BRiscxFmBw`!2Yys1dS7@_")
import json,os,sys,urllib.request,urllib.error
KN=(-21,-19,-12,-8,8,12,19,21)
KG=(-11,-10,-9,-1,1,9,10,11)
BD=(-11,-9,9,11);RD=(-10,-1,1,10);QD=BD+RD
def sq(s): return (ord(s[0])-96)+(int(s[1])+1)*10
def sn(i): return "abcdefgh"[i%10-1]+str(i//10-1)
def on(i): return i%10 not in(0,9) and 21<=i<=98
class Pos: __slots__='bd','sd','cl','ep'
def ps(fen):
 f=fen.split();p=Pos();p.bd=[' ']*120
 for i in range(120):
  if on(i):p.bd[i]='.'
 for r,row in enumerate(f[0].split('/')):
  c=0
  for ch in row:
   if ch.isdigit():c+=int(ch)
   else:p.bd[sq("abcdefgh"[c]+str(8-r))]=ch;c+=1
 p.sd=f[1]=='w'
 p.cl=f[2] if len(f)>2 and f[2]!='-' else ''
 p.ep=sq(f[3]) if len(f)>3 and f[3]!='-' else 0
 return p
def ak(p,i,s):
 b=p.bd
 for d in ((11,9) if s else (-11,-9)):
  if b[i-d]==('P' if s else 'p'):return True
 for d in KN:
  if on(i+d)and b[i+d]==('N' if s else 'n'):return True
 for d in KG:
  if on(i+d)and b[i+d]==('K' if s else 'k'):return True
 for ds,ch in((BD,'BQ' if s else 'bq'),(RD,'RQ' if s else 'rq')):
  for d in ds:
   j=i+d
   while on(j):
    c=b[j]
    if c!='.':
     if c in ch:return True
     break
    j+=d
 return False
def gn(p):
 b=p.bd;s=p.sd;out=[]
 up=10 if s else -10
 foe=str.islower if s else str.isupper
 own=str.isupper if s else str.islower
 pr8=9 if s else 2
 for i in range(21,99):
  if not on(i):continue
  c=b[i]
  if c=='.'or not own(c):continue
  u=c.upper()
  if u=='P':
   j=i+up
   if on(j)and b[j]=='.':
    if j//10==pr8:
     for q in'QRBN':out.append((i,j,q))
    else:
     out.append((i,j,None))
     if i//10==(3 if s else 8)and b[j+up]=='.':out.append((i,j+up,None))
   for d in(up-1,up+1):
    j=i+d
    if not on(j):continue
    t=b[j]
    if t!='.'and foe(t):
     if j//10==pr8:
      for q in'QRBN':out.append((i,j,q))
     else:out.append((i,j,None))
    elif p.ep and j==p.ep:out.append((i,j,'e'))
  elif u=='N':
   for d in KN:
    j=i+d
    if on(j)and(b[j]=='.'or foe(b[j])):out.append((i,j,None))
  elif u=='K':
   for d in KG:
    j=i+d
    if on(j)and(b[j]=='.'or foe(b[j])):out.append((i,j,None))
   if s and i==25:
    if 'K'in p.cl and b[26]=='.'and b[27]=='.'and b[28]=='R'and not ak(p,25,not s)and not ak(p,26,not s)and not ak(p,27,not s):out.append((25,27,None))
    if 'Q'in p.cl and b[24]=='.'and b[23]=='.'and b[22]=='.'and b[21]=='R'and not ak(p,25,not s)and not ak(p,24,not s)and not ak(p,23,not s):out.append((25,23,None))
   if not s and i==95:
    if 'k'in p.cl and b[96]=='.'and b[97]=='.'and b[98]=='r'and not ak(p,95,not s)and not ak(p,96,not s)and not ak(p,97,not s):out.append((95,97,None))
    if 'q'in p.cl and b[94]=='.'and b[93]=='.'and b[92]=='.'and b[91]=='r'and not ak(p,95,not s)and not ak(p,94,not s)and not ak(p,93,not s):out.append((95,93,None))
  else:
   for d in(BD if u=='B'else RD if u=='R'else QD):
    j=i+d
    while on(j):
     t=b[j]
     if t=='.'or foe(t):out.append((i,j,None))
     if t!='.':break
     j+=d
 legal=[]
 k='K'if s else'k'
 for m in out:
  st=mk(p,m)
  if not ak(p,b.index(k),not s):legal.append(m)
  uk(p,m,st)
 return legal
def mk(p,m):
 i,j,q=m;b=p.bd
 st=(b[i],b[j],p.cl,p.ep)
 c=b[i]
 b[j]=c if not q or q=='e'else(q if c.isupper()else q.lower())
 b[i]='.'
 if q=='e':b[j+(-10 if c=='P'else 10)]='.'
 if c in'Kk'and abs(j-i)==2:
  if j==97:b[98]='.';b[96]='r'
  if j==93:b[91]='.';b[94]='r'
  if j==27:b[28]='.';b[26]='R'
  if j==23:b[21]='.';b[24]='R'
 if c in'Pp'and abs(j-i)==20:p.ep=(i+j)//2
 else:p.ep=0
 cr=p.cl
 if c=='K':cr=cr.replace('K','').replace('Q','')
 if c=='k':cr=cr.replace('k','').replace('q','')
 for x,y in((98,'k'),(91,'q'),(28,'K'),(21,'Q')):
  if i==x or j==x:cr=cr.replace(y,'')
 p.cl=cr
 p.sd=not p.sd
 return st
def uk(p,m,st):
 i,j,q=m;b=p.bd
 b[i]=st[0];b[j]=st[1]
 c=st[0]
 if q=='e':b[j+(-10 if c=='P'else 10)]='p'if c=='P'else'P'
 if c in'Kk'and abs(j-i)==2:
  if j==97:b[96]='.';b[98]='r'
  if j==93:b[94]='.';b[91]='r'
  if j==27:b[26]='.';b[28]='R'
  if j==23:b[24]='.';b[21]='R'
 p.cl=st[2];p.ep=st[3]
 p.sd=not p.sd
def T(o): return [6*(int.from_bytes(TB[(o*8+6*i)//8:(o*8+6*i)//8+2],"little")>>(o*8+6*i)%8&63)-190 for i in range(64)]
A=T(0)
B=T(48)
C=T(96)
D=T(144)
F=T(192)
G=T(240)
import json,os,sys,base64
EU=os.environ.get("MAKEFUN_ENV_URL")
V={'P': 82,'N': 337,'B': 365,'R': 477,'Q': 1025,'K': 0}
MT=100000
def T(s):
 return [int(x) for x in s.split(',')]
PST={'P': A,'N': B,'B': C,'R': D,'Q': F,'K': G}
def sqi(i):
 f=i%10 - 1
 r=i // 10 - 1
 return (7 - r)*8+f
def ev(p):
 bd=p.bd
 s=0
 for i in range(21,99):
  if not on(i):
   continue
  c=bd[i]
  if c == '.':
   continue
  u=c.upper()
  idx=sqi(i)
  if not c.isupper():
   idx ^= 56
  v=V[u]+PST[u][idx]
  s += v if c.isupper() else -v
 kt=G
 s += kt[sqi(bd.index('K'))] - kt[sqi(bd.index('k')) ^ 56]
 return s if p.sd else -s
NN=0
cur=None
def msc(m):
 i,j,pr=m
 bd=cur.bd
 t=bd[j]
 s=0
 if t != '.':
  s=10*V[t.upper()] - V[bd[i].upper()]
 if pr and pr != 'e':
  s += V[pr]
 return s
def qs(p,al,bt):
 global NN
 NN += 1
 stn=ev(p)
 if stn >= bt:
  return bt
 if stn > al:
  al=stn
 cs=[m for m in gn(p) if p.bd[m[1]] != '.' or m[2] == 'e']
 cs.sort(key=msc,reverse=True)
 for m in cs:
  st=mk(p,m)
  sc=-qs(p,-bt,-al)
  uk(p,m,st)
  if sc >= bt:
   return bt
  if sc > al:
   al=sc
 return al
TT={}
def nx(p,dp,al,bt):
 global NN
 if dp == 0:
  return qs(p,al,bt)
 NN += 1
 key=(tuple(p.bd),p.sd,p.cl,p.ep)
 e=TT.get(key)
 if e is not None and e[0] >= dp:
  if e[1] == 0:
   return e[2]
  if e[1] == 1 and e[2] >= bt:
   return e[2]
  if e[1] == 2 and e[2] <= al:
   return e[2]
 ki=p.bd.index('K' if p.sd else 'k')
 if dp >= 3 and bt < MT - 1000 and not ak(p,ki,not p.sd):
  e0=p.ep
  p.ep=0
  p.sd=not p.sd
  sc=-nx(p,dp - 3,-bt,-bt+1)
  p.sd=not p.sd
  p.ep=e0
  if sc >= bt:
   return bt
 ms=gn(p)
 if not ms:
  return -MT if ak(p,ki,not p.sd) else 0
 pv=e[3] if e is not None else None
 if pv is not None and pv in ms:
  ms.remove(pv)
  ms.insert(0,pv)
 ms.sort(key=msc,reverse=True)
 best=-MT*2
 bm=None
 for m in ms:
  st=mk(p,m)
  sc=-nx(p,dp - 1,-bt,-al)
  uk(p,m,st)
  if sc > best:
   best=sc
   bm=m
  if sc > al:
   al=sc
  if al >= bt or NN > NC:
   break
 TT[key]=(dp,0 if al < best < bt else (1 if best >= bt else 2),best,bm)
 return best
def bmv(p,cap):
 global NN,NC,cur
 cur=p
 NC=cap
 NN=0
 TT.clear()
 ms=gn(p)
 if not ms:
  return None
 best=ms[0]
 NN=0
 for dp in range(1,10):
  al=-MT*2
  cb=best
  done=True
  ms.sort(key=msc,reverse=True)
  for m in ms:
   st=mk(p,m)
   sc=-nx(p,dp - 1,-MT*2,-al)
   uk(p,m,st)
   if sc > al:
    al=sc
    cb=m
   if NN > NC:
    done=False
    break
  if done or al > MT - 1000:
   best=cb
  if al > MT - 1000 or not done:
   break
 return best
def mu(m):
 i,j,pr=m
 s=sn(i)+sn(j)
 if pr and pr != 'e':
  s += pr.lower()
 return s
from urllib.request import Request as Rq,urlopen as UO
from urllib.error import HTTPError as He
def po(pt,by):
 req=Rq(EU+pt,data=json.dumps(by).encode(),
        headers={"content-type": "application/json"})
 try:
  with UO(req) as res:
   return json.load(res)
 except He as e:
  Q(f"{pt}: HTTP {e.code} {e.read().decode(errors='replace')}")
CAP=24000
def main():
 while True:
  g=po("/game",{})
  if g["status"] == "done":
   break
  while g["status"] == "your_move":
   p=ps(g["fen"])
   lg=g["legal_moves"]
   bm=bmv(p,CAP)
   u=mu(bm) if bm else None
   if u not in lg:
    u=lg[0]
   g=po("/move",{"game": g["game"],"move": u})
main()
