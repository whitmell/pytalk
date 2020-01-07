from collections import defaultdict
import subprocess
from pathlib import Path
import json

from params import *
from ie import *
from nltk.corpus import stopwords

stop_words=set(stopwords.words('english'))
client = OpenIE()

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
  dependencies = []
  triples = []
  sentences = []
  lemmas = []
  tags=[]
  ners=[]
  for i,xss in enumerate(client.extract(text)) :
    lexs,deps,ies=xss
    sent=[]
    lemma=[]
    tag=[]
    ner=[]
    for j,t in enumerate(lexs):
      w,l,p,n=t
      wi=len(l2occ)
      l2occ[l].append((i,j))
      sent.append(w)
      lemma.append(l)
      tag.append(p)
      ner.append(n)
    for t in ies:
      triples.append(t)
    for t in deps:
      dependencies.append(t)
    sentences.append(sent)
    lemmas.append(lemma)
    tags.append(tag)
    ners.append(ner)
  res = (sentences,lemmas,tags,ners,  l2occ,dependencies,triples)
  s = len(sentences)
  l=len(lemmas)
  t=len(tags)
  tt=len(triples)
  n=len(ners)
  d=len(dependencies)
  #tprint('LENS:',s,l,t,tt)
  assert l==s==t==n==d
  if openie : assert t==tt
  return res

def rel_from(id,lemmas,tss):
  def to_lems(ux):
    f,t=ux
    if f>=0:
      for u in range(*ux):
        yield lemma[u]
  rs=[]
  for t in tss[id] :
    sx, vx, ox = t
    lemma = lemmas[id]
    sub = tuple(to_lems(sx))
    rel = tuple(to_lems(vx))
    ob = tuple(to_lems(ox))
    res = (sub, rel, ob)
    rs.append(res)
  yield rs


def deps_from(id,lemmas,deps):
  rs=[]
  for dep in deps[id] :
    lemma = lemmas[id]
    f, r, t = dep
    if t == -1 : target=id
    else: target = lemma[t]
    res = lemma[f],r,target
    rs.append(res)
  yield rs


def show_db(db) :
    sents, lemmas, tags, ners, ls, ds, ts = db
    for id in range(len(ts)) :
      for trip in rel_from(id, lemmas, ts):
         print('TRIPLES:', trip)
    for dep in deps_from(id,lemmas,ds) :
         print('DEPENDS:',dep)
    print('')


def answer_quest(q,db) :
    sentences,lemmas,tags,ners, ls, ds, ts=db
    matches = defaultdict(set)
    q_db=digest(q)
    if trace > 1:
      for x in q_db:
        print(x)
      print('!!!!')
    if trace>1 :
      show_db(q_db)

    _q_sents,q_lemmas,q_tags,_g_ners,_q_ls,_q_ds,q_ts=q_db
    unknowns=[]

    for qj,q_lemma in enumerate(q_lemmas[0]):
       if q_lemma in stop_words or q_lemma in ".?" : continue
       q_tag=q_tags[0][qj]
       ys = ls.get(q_lemma)
       if not ys :
         unknowns.append(q_lemma)
         continue
       for sent,pos in ys:
         tag=tags[sent][pos]
         if stemmer or tag[0] == q_tag[0]:
           matches[sent].add(q_lemma)
         else : print('UNMATCHED LEMMA',q_lemma,q_tag,tag)
    if unknowns: tprint("UNKNOWNS:", unknowns,'\n')
    best=[]
    for (id, shared) in matches.items() :
      sent=sentences[id]
      r=len(shared)+len(shared)/len(sent)
      best.append((r,id,shared,sent))
    best.sort(reverse=True)

    answers=[]
    #print("BEST",len(best),len(lemmas))
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
    tprint('  ', shared, rank,)
  print('')
  tprint('------END-------', '\n')

# helpers

def cleaned(w) :
  if w in ['-LRB-','-lrb-'] : return '('
  if w in ['-RRB-','-rrb-'] : return ')'
  return w

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

def good_tag(tag,starts="NVJ"):
  c=tag[0]
  return c in starts

