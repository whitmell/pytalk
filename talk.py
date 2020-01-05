from collections import defaultdict
import subprocess
from ie import *
from nltk.corpus import stopwords

stop_words=set(stopwords.words('english'))
client = OpenIE()

quiet=True
max_answers=3
trace=1
def tprint(*args) :
  if trace : print(*args)

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
  lemmas = []
  tags=[]
  for i,xss in enumerate(client.extract(text)) :
    lexs,deps,ies=xss
    sent=[]
    lemma=[]
    tag=[]
    for j,t in enumerate(lexs):
      w,l,p=t
      wi=len(l2occ)
      l2occ[l].append((i,j))
      sent.append(w)
      lemma.append(l)
      tag.append(p)
    for t in ies:
      triples.append(t)
    for t in deps:
      dependencies.append(t)
    sentences.append(sent)
    lemmas.append(lemma)
    tags.append(tag)
  return (sentences,lemmas,tags, l2occ,dependencies,triples)

def validate(xs):
  for x in xs:
    q_tag = x[2]
    if good_tag(q_tag):
      yield q_tag

def rel_from(id,ls,ts):
  s,v,o=ts[id]
  #lemma=ls[id]
  #print(lemma)
  #sx = [lemmas[id][j] for j in range(*s)]
  #print('REL', s)
  ##print(ls)
  #ls=lemmas[id]
  #print(lex)
  #print([j for j in range(*s)])





def answer_quest(q,db) :
    sentences,lemmas,tags, ls, ds, ts=db
    rel_from(0,lemmas,ts)
    matches = defaultdict(set)
    q_db=digest(q)
    if trace > 1:
      for x in q_db:
        print(x)
      print('!!!!')
    _q_sents,q_lemmas,q_tags,_q_ls,_q_ds,_q_ts=q_db

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
         else : print('LEMMA',q_lemma,q_tag,tag)
    if unknowns: tprint("UNKNOWNS:", unknowns)
    best=[]
    for (id, shared) in matches.items() :
      sent=sentences[id]
      r=len(shared)+len(shared)/len(sent)
      best.append((r,id,shared,sent))
    best.sort(reverse=True)
    answers=[]
    for i,b in enumerate(best):
      if i<max_answers :
        rank, id, shared, sent = b
        answers.append((id,sent,rank,shared))
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
  tprint('----- QUERY ----\n')
  say(q)
  print('')
  for info, sent, rank, shared in answer_quest(q, db):
    print(info,end=': ')
    say(nice(sent))
    tprint('  ', shared, rank,)
  tprint('\n', '------END-------', '\n')

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

# tests
def go() :
  with open('examples/texas_quest.txt','r') as f:
    qs=list(l[:-1] for l in f)
    query('test.json',qs)

def go1() :
  jsave('examples/texas.txt','test.json')
  query('test.json', #'examples/texas.txt',
        ["Who fought in the battle of San Antonio?",
         "Who fired the cannons?",
         "Who was Stephen Austin?"
        ])

def ggo() :
  with open('examples/geo_quest.txt','r') as f:
    qs=list(l[:-1] for l in f)
    query('test.json',qs)


def ggo1() :
  jsave('examples/geo.txt','geo_test.json')
  query('test.json', #'examples/texas.txt',
        ["Who fought in the battle of San Antonio?",
         "Who fired the cannons?",
         "Who was Stephen Austin?"
        ])


def igo() :
  query('test.json', [])

ggo()


