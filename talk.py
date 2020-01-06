from collections import defaultdict
import subprocess
from ie import *
from nltk.corpus import stopwords

stop_words=set(stopwords.words('english'))
client = OpenIE()

quiet=False
max_answers=3
trace=0
def tprint(*args) :
  if trace : print(*args)

def say(what) :
  print(what)
  if not quiet : subprocess.run(["say", what])

def load(infile) :
  tprint('LOADING:',infile)
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
  res = (sentences,lemmas,tags, l2occ,dependencies,triples)
  s = len(sentences)
  l=len(lemmas)
  t=len(tags)
  tt=len(triples)
  #tprint('LENS:',s,l,t,tt)
  assert l==s==t==tt
  return res

def rel_from(id,lemmas,tags,tss):
  def to_lems(ux):
    for u in range(*ux):
      yield lemma[u]

  rs=[]
  for t in tss[id] :
    sx, vx, ox = t
    lemma = lemmas[id]
    tag = tags[id]
    sub = tuple(to_lems(sx))
    rel = tuple(to_lems(vx))
    ob = tuple(to_lems(ox))
    res = (sub, rel, ob)
    rs.append(res)
  yield rs




def answer_quest(q,db) :
    sentences,lemmas,tags, ls, ds, ts=db
    if trace>2: #TODO
      for i in range(len(lemmas)) :
        for trip in rel_from(i,lemmas,tags,ts) :
          tprint('TRIP',len(trip))
    matches = defaultdict(set)
    q_db=digest(q)
    if trace > 1:
      for x in q_db:
        print(x)
      print('!!!!')
    _q_sents,q_lemmas,q_tags,_q_ls,_q_ds,q_ts=q_db

    unknowns=[]
    if trace> 2: # TODO
       for trip in rel_from(0,q_lemmas,q_tags,q_ts) : print('QTRIP',trip)
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
        answers.append((id,sent,round(rank,2),shared))
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
  print('')
  tprint('------END-------', '\n')

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
  jsave('examples/geo.txt','test.json')
  ggo()

def igo() :
  query('test.json', [])

def test() :
    jsave('examples/test.txt', 'test.json')
    with open('examples/test_quest.txt', 'r') as f:
      qs = list(l[:-1] for l in f)
      query('test.json', qs)


#test()


