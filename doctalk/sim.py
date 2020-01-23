from nltk.corpus import wordnet as wn
import math

# basic wordnet relations
  
def wn_hyper(k,w,t) :
  i=1
  for s in wn.synsets(w) :
    for h in s.hypernyms() :
      r = s2w(h,t)
      if r : 
        yield r
        i+=1
        if i >k : return

def wn_hypo(k,w,t) :
  i=1
  for s in wn.synsets(w) :
    for h in s.hyponyms() :
      r = s2w(h,t)
      if r : 
        yield r
        i+=1
        if i >k : return
 
def wn_mero(k,w,t) :
  i=1
  for s in wn.synsets(w) :
    for h in s.part_meronyms() :
      r = s2w(h,t)
      if r : 
        yield r
        i+=1
        if i >k : return

def wn_holo(k,w,t) :
  i=1
  for s in wn.synsets(w) :
    for h in s.part_holonyms() :
      r = s2w(h,t)
      if r : 
        yield r
        i+=1
        if i >k : return

#  less useful but potentially interesting for weak proximity
def wn_syn(k,w,t) :
  i=1
  for s in wn.synsets(w) : 
    r = s2w(s,t)
    if r and r != w : 
      yield r
      i+=1
      if i >=k : return

def syns(k,w,t) :
  tag='.'+t+'.'
  synonyms = set()
  for syn in wn.synsets(w):
    if not tag in syn.name() : continue
    for l in syn.lemmas():
      print('  ',l)
      s=l.name()
      s=s.replace('_', ' ')
      synonyms.add(s)
      if len(synonyms) >=k : return synonyms
  return synonyms

def s2w(s,t) :
  n = s.name()
  (w,tw,_) = n.split('.')
  if t==tw : return w.replace('_',' ')
  return None
  

def ttt() :
  print(syns(3,'dog','n'))
      
######
