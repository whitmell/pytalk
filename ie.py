import sys
import json
from nltk.stem import PorterStemmer

#stemmer=None
stemmer=PorterStemmer()

annotators=['tokenize','ssplit','pos','lemma','ner',
            'parse','depparse', 'natlog', 'openie']

def ies_of(sentence):
  for triple in sentence['openie']:
    s = triple['subjectSpan']
    v = triple['relationSpan']
    o = triple['objectSpan']
    yield tuple(s),tuple(v),tuple(o)

def deps_of(sentence):
      for x in sentence['enhancedPlusPlusDependencies'] :
        r=x['dep']
        t=x['governor']
        f=x['dependent']
        yield (f,r,t)

def word_ies_of(sentence,lemma=True):
  ts=[]
  toks = sentence['tokens']
  for tok in toks:
    #print([x for x in tok])
    if lemma:
      w=tok['lemma']
      if stemmer: w = stemmer.stem(w)
    else : w=tok['word']
    ts.append(w)

  def svos() :
    for ie in ies_of(sentence) :
      s,v,o=ie
      s=tuple(ts[i] for i in range(*s))
      v=tuple(ts[i] for i in range(*v))
      o=tuple(ts[i] for i in range(*o))
      yield s,v,o

  return tuple(ts),tuple(svos())

def lexs_of(sentence):
    toks = sentence['tokens']
    for tok in toks:
      #print([x for x in tok])
      #p = tok['index']
      w = tok['word']
      l = tok['lemma']
      if stemmer : l=stemmer.stem(l)
      t = tok['pos']
      yield ( w, l, t)

def to_json(infile,outfile,lemma=True):
  client = OpenIE()
  with open(infile,'r') as f : text=f.read()
  all=list(client.word_ies(text,lemma=lemma))
  with open(outfile,'w') as g :
    json.dump(all,g,indent=2)


def to_full_json(infile,outfile):
  client = OpenIE()
  with open(infile,'r') as f : text=f.read()
  with open(outfile, 'w') as g:
    xs=[x for x in client.extract(text)]
    json.dump(xs,g,indent=2)


def clean(text) :
  def trim(char):
    if ord(char) < 7 or ord(char) > 127:
      return ''
    elif char in "()[]\'":
      return " "
    else:
      return char
  return "".join(map(trim,text))


def clean_text(text) :
  text=text.replace('..',' ')
  #print("LLL",len(text),text)
  return text



class OpenIE:
  def __init__(self, core_nlp_version = '2018-10-05'):
    from stanfordnlp.server import CoreNLPClient
    self.client = CoreNLPClient(start_server=False)

  def __enter__(self): return self
  def __exit__(self, exc_type, exc_val, exc_tb): pass
  def __del__(self): self.client.stop()

  def step(self,text) :
      core_nlp_output = self.client.annotate(text=text,
                      annotators=annotators, output_format='json')
      for sentence in core_nlp_output['sentences']:
        lexs=tuple(lexs_of(sentence))
        deps=tuple(deps_of(sentence))
        ies=tuple(ies_of(sentence))
        yield lexs,deps,ies

  def extract(self, text):
    tail=clean_text(text)
    while tail:
      chunk=10000
      head=tail[0:chunk]
      tail=tail[chunk:]
      yield from self.step(head)

  def word_ies(self,text,lemma=True) :
    core_nlp_output = self.client.annotate(text=text,
        annotators=annotators, output_format='json')
    for sentence in core_nlp_output['sentences'] :
      #print([x for x in sentence])
      yield tuple(word_ies_of(sentence,lemma=lemma))

def to_db(infile):
  client = OpenIE()
  with open(infile,'r') as f : text=f.read()
  for x in client.extract(text) :
    print(x)




def go() :
  to_json('examples/bfr.txt','test.json')

def fgo() :
  to_full_json('examples/texas.txt','test.json')


def test() :
  to_db('examples/test.txt')

if __name__=="__main__" :
  #go()
  test()
  #pass
