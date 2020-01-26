from collections import defaultdict
import subprocess
from pathlib import Path
import math
import networkx as nx
import statistics as stat
from pprint import pprint

from .nlp import *
from .sim import *
from .vis import pshow,gshow

client = NLPclient()


def run_with(fname,query=True,show=show_pics) :
  '''
  Activates dialog about document in <fname>.txt with questions
  in <fname>_quests.txt
  Assumes stanford corenlp server listening on port 9000
  with annotators listed in params.py  available.
  '''
  t = Talker(from_file=fname+'.txt')
  t.show_all()
  if query:
    t.query_with(fname+'_quest.txt')
    pshow(t,file_name=fname+"_quest",show=show)


def chat_about(fname,qs=None,show_pics=show_pics) :
  t = Talker(from_file=fname + '.txt')
  t.show_all()
  t.query_with(qs)



def tprint(*args) :
  if trace : print(*args)

def say(what) :
  print(what)
  if not quiet : subprocess.run(["say", what])

def tload(infile) :
  tprint('LOADING:',infile,'\n')
  with open(infile, 'r') as f: text = f.read()
  return digest(text)

def jload(infile) :
  with open(infile, 'r') as f:
    res = json.load(f)
    return res

def jsave(infile,outfile):
  d=tload(infile)
  with open(outfile,'w') as g:
    json.dump(d,g,indent=0)

def exists_file(fname) :
  path = Path(fname)
  return path.is_file()

def load(fname) :
  if fname[-4:]==".txt":
    if force:
      db = tload(fname)
    else :
      jfname=fname[:-4]+".json"
      if not exists_file(jfname) :
        jsave(fname,jfname)
      db=jload(jfname)
  else:
    db = jload(fname)
  return db

def get_quests(qs) :
  if not isinstance(qs,list) :
    qfname=qs
    with open(qfname,'r') as f:
      qs = list(l.strip() for l in f)
  return qs

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
    d=(tuple(sent),tuple(lemma),tuple(tag),
       tuple(ner),tuple(deps),tuple(ies))
    sent_data.append(d)
  #tprint('DIGESTED')
  return sent_data,l2occ

SENT,LEMMA,TAG,NER,DEP,IE=0,1,2,3,4,5

def rel_from(d):
  def to_lems(ux):
    f,t=ux
    if f>=0:
      for u in range(*ux):
        yield lemma[u],tag[u]
  rs,svos=set(),set()
  for ts in d[IE] :
    for t in ts :
      sx, vx, ox = t
      lemma = d[LEMMA]
      tag=d[TAG]
      sub = tuple(to_lems(sx))
      rel = tuple(to_lems(vx))
      ob = tuple(to_lems(ox))
      res = (sub, rel, ob)
      s=()
      for l,tl in sub:
        if tl[0]=='N' :
          s=l
      o=()
      for l, tl in ob:
        if tl[0] == 'N':
          o = l
      v=()
      for l, tl in rel:
        if tl[0] == 'V':
          v = l
      rs.add(res)
      svo=s,v,o
      if () in svo : continue
      svos.add(svo)

  return tuple(rs),tuple(svos)

def dep_from(id,d):
  deps=d[DEP]
  lemmas=d[LEMMA]
  tags=d[TAG]
  for dep in deps :
    f, r, t = dep
    if t == -1 : target,ttag=id,'SENT'
    else: target,ttag = lemmas[t],tags[t]
    res = lemmas[f],tags[f],r,target,ttag
    yield res

def deps_from(id,d) :
  return tuple(t for t in dep_from(id,d))

def comp_from(id,d) :
  for x in dep_from(id,d) :
    f,tf,rel,t,tt=x
    #ppp(f,t)
    if (rel == 'compound' or rel == 'amod') and \
       good_word(f) and good_word(t) and \
       good_tag(tf) and good_tag(tt) :
      yield (f,t)

def comps_from(id,d) :
  return tuple(t for t in comp_from(id,d) if t)

def to_edges(db) :
  sent_data,l2occ=db
  for id,sd in enumerate(sent_data) :
    for dep in dep_from(id,sd):
      f,f_,r,t,t_=dep
      if r == 'punct': continue
      elif r in ['nsubj','dobj','iobj'] or t_[0]=='V':
        yield (id, f) # sent to predicate
        yield (t,f) # pred to arg
        yield (f,id) # arg to sent
      elif f in stop_words or t in stop_words:
        continue
      elif r=='ROOT' :
        yield (t,f)
      else :
        yield (f,t)
    if compounds :
      for ft in comps_from(id, sd):
          f,t=ft
          yield f, ft #parts to compound
          yield t, ft
          yield ft,id # compound to sent
          yield ft,ft # to self


def get_avg_len(db) :
  sent_data,_=db
  lens=[len(x[LEMMA]) for x in sent_data]
  n=len(lens)
  s=sum(lens)
  return round(s/n)

def to_graph(db,personalization=None) :
  g = nx.DiGraph()
  for e in to_edges(db) :
    f,t=e
    g.add_edge(f,t)
  try :
     pr=nx.pagerank(g,personalization=personalization)
  except :
    n=g.number_of_nodes()
    pr=dict()
    for l in db[1] : pr[l]=1/n
  return g,pr

def rank_sort(pr) :
  by_rank=[(x,r) for (x,r) in pr.items()]
  by_rank.sort(key=lambda x : x[1],reverse=True)
  return by_rank

def ners_from(d):
  ners=[]
  for j, ner in enumerate(d[NER]):
    lemma = d[LEMMA][j]
    if ner != 'O': ners.append((lemma,ner))
  return tuple(ners)

def materialize(db) :
  sent_data,l2occ= db
  for i,d in enumerate(sent_data) :
      rels,svos = rel_from(d)
      deps=deps_from(i,d)
      comps=comps_from(i,d) # or directly from deps
      ners=ners_from(d)
      yield tuple(d[SENT]),tuple(d[LEMMA]),tuple(d[TAG]),\
            ners,rels,svos,deps,comps

def wn_from(l2occ) :
  for w in l2occ :
    for s,v,o in wn_svo(2,10,w,'n') :
      if l2occ.get(o) :
        yield (s,v,o)

def v2rel(v) :
  if v=='be' : return 'is_a'
  return v

def e2rel(e) :
  if e=='MISC' : return 'entity'
  return e.lower()




def file_svos(fname) :
  t=Talker(from_file=fname)
  yield from t.to_svos().items()

def answer_quest(q,talker) :
    db=talker.db
    sent_data,l2occ=db
    matches = defaultdict(set)
    nears=defaultdict(set)
    answerer=Talker(from_text=q)
    q_sent_data,q_l2occ=answerer.db
    #gshow(answerer.g)
    unknowns=[]
    for j,q_lemma in enumerate(q_sent_data[0][LEMMA]):
       q_tag=q_sent_data[0][TAG][j]
       if q_tag[0] not in "NVJ" : continue # ppp(q_lemma,q_tag)
       if q_lemma in stop_words or q_lemma in ".?" : continue
       ys = l2occ.get(q_lemma)
       if not ys :
         unknowns.append(q_lemma)
       else :
         for sent,_pos in ys:
           matches[sent].add(q_lemma)
       if expand_query > 0:
         related = wn_all(expand_query, 10, q_lemma, wn_tag(q_tag))
         for r_lemma in related:
           if r_lemma in stop_words : continue
           zs=l2occ.get(r_lemma)
           if not zs : continue
           for r_sent,_r_pos in zs :
             nears[r_sent].add((r_lemma,q_lemma))
           if zs and not ys :
             if q_lemma in unknowns : unknowns.pop()
           tprint('EXPANDED:',q_lemma,'-->',r_lemma)
    if unknowns: tprint("UNKNOWNS:", unknowns,'\n')

    best=[]
    if pers :
      d={x:r for x,r in answerer.pr.items() if x not in stop_words}
      '''
      for near in nears.values() :
         for n,l in near :
           lr=d.get(l)
           if lr :
             d[n]=math.log(1+lr)
             #ppp(n,l,lr)
      '''
      talker.pr=nx.pagerank(talker.g,personalization=d)

    for (id, shared) in matches.items() :
      sent=sent_data[id][SENT]
      r=answer_rank(id,shared,sent,talker,expanded=0)
      best.append((r,id,shared,sent))
      #ppp('MATCH', id,shared, r)

    for (id,shared_source) in nears.items() :
      shared = {x for x,_ in shared_source}
      sent = sent_data[id][SENT]
      r = answer_rank(id, shared, sent, talker,expanded=1)
      best.append((r, id, shared, sent))
      #ppp('EXPAND', id,shared, r)

    best.sort(reverse=True)

    answers=[]
    for i,b in enumerate(best):
      if i >= max_answers : break
      rank, id, shared, sent = b
      answers.append((id,sent,round(rank,3),shared))
    if not answers_by_rank : answers.sort()
    return answers

def sigmoid(x): return 1 / (1 + math.exp(-x))

def answer_rank(id,shared,sent,talker,expanded=0) :

  lshared = len(shared)
  if not lshared : return 0

  sent_count=len(talker.db[0])
  word_count=len(talker.db[1])

  lsent = len(sent)
  lavg=talker.avg_len
  srank=talker.pr.get(id)


  nrank=normalize_sent(srank,lsent,lavg)

  if nrank==0 : return 0

  def get_occ_count(x): return len(talker.db[1].get(x))

  unusual = sigmoid(1 - stat.harmonic_mean(
    get_occ_count(x) for x in shared) / sent_count)

  important=math.exp(nrank)

  # #r=stat.harmonic_mean((lshared,important,unusual))
  r=lshared*important*unusual

  if expanded : r=r/2

  #ppp('RANKS:',10000*srank,'-->',10000*nrank,lsent,lavg)
  #ppp('HOW  :', id, lshared, unusual, important, shared,'--->',r)

  #r=math.tanh(r)
  return r

def query_with(talker,qs_or_fname)     :
  if isinstance(qs_or_fname,str) :
    qs = get_quests(qs_or_fname) # file name
  else :
    qs=qs_or_fname # list of questions or None
  if qs:
    for q in qs :
      if not q :break
      interact(q,talker)
  else:
    while True:
      q=input('> ')
      if not q : break
      interact(q,talker)

def interact(q,talker):
  tprint('----- QUERY ----\n')
  say(q)
  print('')
  ### answer is computed here ###
  for info, sent, rank, shared in answer_quest(q, talker):
    print(info,end=': ')
    say(nice(sent))
    tprint('  ', shared, rank)
  print('')
  tprint('------END-------', '\n')

class Talker :
  def __init__(self,from_file=None,from_text=None,
               sk=sum_count,wk=key_count,show=show_pics):
    self.from_file=from_file
    if from_file:
       self.db=load(from_file)
       self.from_file=from_file
    elif from_text :
       self.db=digest(from_text)
    else :
      assert from_file or from_text
    self.sum_count=sk
    self.key_count=wk
    self.avg_len = get_avg_len(self.db)
    self.g,self.pr=to_graph(self.db)
    #self.get_sum_and_words(sk,wk)
    self.summary, self.keywords = self.extract_content(sk, wk)

  def query_with(self,qs):
    query_with(self,qs)

  def get_tagged(self,w):
    l2occ=self.db[1]
    sent_data=self.db[0]
    occs=l2occ.get(w)
    tags=set()
    words=set()
    for i,j in occs:
      word = sent_data[i][SENT][j]
      tag=sent_data[i][TAG][j]
      words.add(word)
      tags.add(tag)
    return words,tags

  def extract_content(self,sk,wk):

    def nice_word(x,good_tags='N') :
      ws, tags = self.get_tagged(x)
      ncount = 0
      for tag in tags:
        if tag[0] in good_tags:
          ncount += 1
      if ncount > len(tags) // 2:
        cx = x.capitalize()
        if cx in ws: x = cx
        return x
      else:
        return None

    sents,words=[],[]

    npr=dict()
    for x,r in self.pr.items() :
      if isinstance(x,int) :
        ws = self.db[0][x][SENT]
        r=normalize_sent(r,len(ws),self.avg_len)
      npr[x]=r
    by_rank=rank_sort(npr)
    for i  in range(len(by_rank)):
      x,r=by_rank[i]
      if sk and isinstance(x,int) :
        ws=self.db[0][x][SENT]
        sk-=1
        sents.append((r,x,ws))
      elif wk and good_word(x) :
        x=nice_word(x)
        if x:
          wk -= 1
          words.append(x)
      elif wk and isinstance(x,tuple) :
          x=tuple(map(nice_word,x))
          if all(x) :
            wk -= 1
            words.append(x)
    sents.sort(key=lambda x: x[1])
    summary=[(r,x,nice(ws)) for (r,x,ws) in sents]
    self.by_rank=by_rank # to be used when needed
    return summary,words

  def to_svos(self):
    sent_data, l2occ = self.db
    d = defaultdict(set)
    for i, data in enumerate(sent_data):
      rels, svos = rel_from(data)
      comps = comps_from(i, data)  # or directly from deps
      ners = ners_from(data)
      for s, v, o in svos:
        if good_word(s) and good_word(o) :
           d[(s, v2rel(v), o)].add(i)
      for x, e in ners:
        d[(x, 'is_a', e2rel(e))].add(i)

      for a, b in comps:
        c = join(a, b)
        d[(a, 'as_in', c)].add(i)
        d[(b, 'as_in', c)].add(i)

    for svo in wn_from(l2occ):
      s,v,o=svo
      occs=set()
      for  id,_ in l2occ.get(s) :
        occs.add(id)
      for id, _ in l2occ.get(o):
        occs.add(id)
      d[svo]=occs

    return d

  def show_summary(self):
    say('SUMMARY:')
    for r,x,sent in self.summary:
      print(x,end=': ')
      say(sent)
    print('')

  def show_keywords(self):
    print('KEYWORDS:')
    print(self.keywords)
    print('')

  def show_rels(self):
    print('RELATIONS:')
    for svoi in self.to_svos().items():
       print(svoi)


  def show_all(self):
    self.show_summary()
    self.show_keywords()
    if show_rels:
      self.show_rels()
    if show_pics and self.from_file:
      pshow(self, file_name=self.from_file)

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


def normalize_sent(r,sent_len,avg_len):
  if sent_len > 2*avg_len or sent_len < avg_len/2 :
    return 0
  factor =  1/(1+abs(sent_len-avg_len)+sent_len)
  #ppp("NORM:",factor,r,sent_len,avg_len)
  return r*factor


def good_word(w) :
  return isinstance(w,str) and w.isalpha() and w not in stop_words

def good_tag(tag,starts="NVJA"):
  c=tag[0]
  return c in starts
