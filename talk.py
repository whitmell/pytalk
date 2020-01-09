from collections import defaultdict
import subprocess
from pathlib import Path
import json
import math

from params import *
from nlp import *
from nltk.corpus import stopwords

stop_words=set(stopwords.words('english'))
stop_words.union({'|(){}[]'})
client = NLPclient()

def tprint(*args) :
  if trace : print(*args)

def say(what) :
  print(what)
  if not quiet : subprocess.run(["say", what])

def load(infile) :
  tprint('LOADING:',infile,'\n')
  with open(infile, 'r') as f: text = f.read()
  return digest(text)

def jload(infile) :
  with open(infile, 'r') as f:
    return json.load(f)

def jsave(infile,outfile):
  d=load(infile)
  with open(outfile,'w') as g:
    json.dump(d,g,indent=0)

def get_db_and_quests(fname,qs) :
  if fname[-4:]==".txt":
    if force:
      db = load(fname)
    else :
      jfname=fname[:-4]+".json"
      my_file = Path(jfname)
      if not my_file.is_file() :
         jsave(fname,jfname)
      db=jload(jfname)
  else:
    db = jload(fname)
  if not isinstance(qs,list) :
    qfname=qs
    with open(qfname,'r') as f:
      qs = list(l.strip() for l in f)
  return (db,qs)

def digest(text) :
  l2occ = defaultdict(list)
  sent_data=[]
  for i,xss in enumerate(client.extract(text)) :
    lexs,deps,ies=xss
    sent,lemma,tag,ner=[],[],[],[]
    for j,t in enumerate(lexs):
      w,l,p,n=t
      wi=len(l2occ)
      l2occ[l].append((i,j))
      sent.append(w)
      lemma.append(l)
      tag.append(p)
      ner.append(n)
    d=(tuple(sent),tuple(lemma),tuple(tag),tuple(ner),tuple(deps),tuple(ies))
    sent_data.append(d)
  return sent_data,l2occ

def rel_from(d):
  def to_lems(ux):
    f,t=ux
    if f>=0:
      for u in range(*ux):
        yield lemma[u]
  rs=[]
  for ts in d[IE] :
    for t in ts :
      sx, vx, ox = t
      lemma = d[LEMMA]
      sub = tuple(to_lems(sx))
      rel = tuple(to_lems(vx))
      ob = tuple(to_lems(ox))
      res = (sub, rel, ob)
      rs.append(res)
  yield rs

def deps_from(id,d):
  rs=[]
  deps=d[DEP]
  lemmas=d[LEMMA]
  for dep in deps :
    f, r, t = dep
    if t == -1 : target=id
    else: target = lemmas[t]
    res = lemmas[f],r,target
    rs.append(res)
  yield rs

SENT,LEMMA,TAG,NER,DEP,IE=0,1,2,3,4,5

def ners_from(d):
  ners=[]
  for j, ner in enumerate(d[NER]):
    lemma = d[LEMMA][j]
    if ner != 'O': ners.append((lemma,ner))
  return ners

def show_db(db) :
    l2occ,sent_data = db
    for i,d in enumerate(sent_data) :
      for trip in rel_from(d): print('TRIPLES:', trip)
      for dep in deps_from(i,d) : print('DEPENDS:',dep)
      print("NERS",ners_from(d))
    print('')

def answer_quest(q,db) :
    sent_data,l2occ=db
    matches = defaultdict(set)
    q_sent_data,q_l2occ=digest(q)
    unknowns=[]
    for q_lemma in q_sent_data[0][LEMMA]:
       if q_lemma in stop_words or q_lemma in ".?" : continue
       ys = l2occ.get(q_lemma)
       if not ys :
         unknowns.append(q_lemma)
         continue
       for sent,pos in ys:
         matches[sent].add(q_lemma)
         #else : print('UNMATCHED LEMMA',q_lemma,q_tag,tag)
    if unknowns: tprint("UNKNOWNS:", unknowns,'\n')
    best=[]
    for (id, shared) in matches.items() :
      sent=sent_data[id][SENT]
      l=len(shared)
      ls=len(sent)
      r=l/(1+math.log(ls/(l*l)))
      best.append((r,id,shared,sent))
    best.sort(reverse=True)

    answers=[]
    for i,b in enumerate(best):
      if i >= max_answers : break
      rank, id, shared, sent = b
      answers.append((id,sent,round(rank,2),shared))
    answers.sort()
    return answers

def query(fname,qs) :
  db,qs=get_db_and_quests(fname,qs)
  if trace > 1:
    show_db(db)
  if qs:
    for q in qs : interact(q,db)
  else:
    while True:
      q=input('> ')
      if not q : break
      interact(q,db)

def interact(q,db):
  tprint('----- QUERY ----\n')
  say(q)
  print('')
  for info, sent, rank, shared in answer_quest(q, db):
    print(info,end=': ')
    say(nice(sent))
    tprint('  ', shared, rank)
  print('')
  tprint('------END-------', '\n')

# helpers

def nice(ws) :
  ws=[cleaned(w) for w in ws]
  sent=" ".join(ws)
  #print(sent)
  sent=sent.replace(" 's","'s")
  sent=sent.replace(" ,",",")
  sent=sent.replace(" .",".")
  sent = sent.replace('``', '"')
  sent = sent.replace("''", '"')
  return sent

def good_tag(tag,starts="NVJA"):
  c=tag[0]
  return c in starts

