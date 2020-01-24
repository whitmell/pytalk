from nltk.corpus import wordnet as wn

# basic wordnet relations
  
def wn_hyper(k,w,t) : return wn_rel(hypers, 2, k, w, t)

def wn_hypo(k,w,t) : return wn_rel(hypos, 2, k, w, t)

def wn_mero(k,w,t) : return wn_rel(meros, 2, k, w, t)

def wn_holo(k,w,t) : return wn_rel(holos, 2, k, w, t)

def wn_syn(k,w,t) : return wn_rel(id, 2, k, w, t)

def wn_all(n,k,w,t) :
  res=wn_rel(id, n, k, w, t)
  for r in (hypers,hypos,meros,holos) :
    res.update(wn_rel(r,n,k,w,t))
  return res



def id(w) : return [w]

def hypos(s) : return s.hyponyms()

def hypers(s) : return s.hypernyms()

def meros(s) : return s.part_meronyms()

def holos(s) : return s.part_holonyms()

#  ADJ,ADJ_SAT, ADV, NOUN, VERB = 'a','s', 'r', 'n', 'v'

def wn_tag(T) :
  c=T[0].lower()
  if c in 'nvr' : return c
  elif c == 'j' : return 'a'
  else : return None

def wn_rel(f,n,k,w,t) :
  related = set()
  for i,syns in enumerate(wn.synsets(w,pos=t)):
    if i>=n : break
    for j,syn in enumerate(f(syns)) :
      if j>=n : break
      #print('!!!!!',syn)
      for l in syn.lemmas():
        #print('  ',l)
        s=l.name()
        if w == s : continue
        s=s.replace('_', ' ')
        related.add(s)
        if len(related) >=k : return related
  return related

def simtest() :
  w,tag='bank','n'
  print(wn_rel(id,2,300,w,tag))
  print(wn_rel(hypers, 2, 300, w, tag))
  print(wn_rel(hypos, 2, 300, w, tag))
  print(wn_rel(meros, 2, 300, w, tag))
  print(wn_rel(holos, 2, 300, w, tag))
  print('')
  print(wn_all(2,3,w,tag))
      
######
