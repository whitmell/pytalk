from collections import defaultdict
import subprocess
from doctalk.nlp import *
from nltk.corpus import stopwords

stop_words=set(stopwords.words('english'))
client = OpenIE()

quiet=True
max_answers=4

def say(what) :
  print(what)
  if not quiet : subprocess.run(["say", what])

def load(infile) :
  with open(infile, 'r') as f: text = f.read()
  return digest(text)

def jload(infile) :
  with open(infile, 'r') as f:
    return json.load(f)

def jsave(infile,outfile):
  d=load(infile)
  import json
  with open(outfile,'w') as g:
    json.dump(d,g,indent=0)

def digest(text) :
  l2occ = defaultdict(list)
  dependencies = []
  triples = []
  sentences = []
  lemmas=[]
  tags=[]
  for i,xss in enumerate(client.extract(text)) :
    lexs,deps,ies=xss
    sent=[]
    for j,t in enumerate(lexs):
      w,l,p=t
      wi=len(l2occ)
      l2occ[l].append((i,j,p))
      sent.append(w)
    for t in ies:
      triples.append(t)
    for t in deps:
      dependencies.append(t)
    sentences.append(sent)
  return (sentences,l2occ,dependencies,triples)

def lems(l2occ) :
  return tuple(l2occ.keys())

def validate(xs):
  for x in xs:
    q_tag = x[2]
    if good_tag(q_tag):
      yield q_tag

def rel_from(id,lemmas,ts):
  s,v,o=ts[id]
  lemma=lemmas[id]
  sx = [lemmas[id][j] for j in range(*s)]
  #print('REL', s)
  ##print(ls)
  #ls=lemmas[id]
  #print(lex)
  #print([j for j in range(*s)])





def answer_quest(q,db) :
    sentences, ls, ds, ts=db
    lemmas=lems(ls)
    rel_from(0,lemmas,ts)
    matches = defaultdict(set)
    q_sents,q_ls,q_ds,q_ts=digest(q)
    unknowns=[]
    for lemma,xs in q_ls.items():
       if lemma in stop_words : continue
       ys = ls.get(lemma)
       if not ys :
         unknowns.append(lemma)
         continue
       q_tags=set(validate(xs))
       tags=validate(ys)
       if q_tags.intersection(tags) :
         for y in ys:
           sent,pos,tag=y
           matches[sent].add(lemma)
    if unknowns: print("UNKNOWNS:", unknowns)
    best=[]
    for (id, shared) in matches.items() :
      sent=sentences[id]
      r=len(shared)+len(shared)/len(sent)
      best.append((r,id,shared,sent))
    best.sort(reverse=True)
    answers=[]
    for i,b in enumerate(best):
      if i<max_answers :
        _rank, id, _shared, sent = b
        answers.append((id,sent))
    answers.sort()

    return answers

def query(fname,qs) :
  if fname[-4:]==".txt":
     db=load(fname)
  else :
    db = jload(fname)
  if qs:
    for q in qs : interact(q,db)
  else:
    while True:
      q=input('> ')
      if not q : break
      interact(q,db)

def interact(q,db):
  print('----- QUERY ----\n')
  say(q)
  print('')
  for _, sent in answer_quest(q, db):
    say(nice(sent))
  print('\n', '------END-------', '\n')

def nice(ws) :
  sent=" ".join(ws)
  #print(sent)
  sent=sent.replace(" 's","'s")
  sent=sent.replace(" ,",",")
  sent=sent.replace(" .",".")
  return sent

def good_tag(tag,starts="NVJ"):
  c=tag[0]
  return c in starts

# tests

def go1() :
  jsave('examples/texas.txt','test.json')
  query('test.json', #'examples/texas.txt',
        ["Who fought in the battle of San Antonio?",
         "Who fired the cannons?",
         "Who was Stephen Austin?"
        ])

def go() :
  with open('examples/texas_quest.txt','r') as f:
    qs=list(l[:-1] for l in f)
    query('test.json',qs)

def igo() :
  query('test.json', [])

go()


