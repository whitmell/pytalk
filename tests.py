import glob
import os
from talk import *

doc_dir="examples/"
doc_files = sorted(glob.glob(doc_dir+"*.txt"))
quest_files = sorted(glob.glob(doc_dir+"*_quest.txt"))

def quest2doc(qf) :
  return qf.replace('_quest.txt','.txt')

def process_docs() :
  for quest_file in quest_files :
    process_doc(quest_file)

def process_doc(quest_file) :
    print(quest_file)
    doc_file=quest2doc(quest_file)
    print(doc_file,'-->',quest_file,'?')
    query(doc_file,quest_file)


#clean files at given directory path
def clean_path(path) :
  os.makedirs(path,exist_ok=True)

  files = glob.glob(path+"/*")
  for f in files:
    os.remove(f)

def json_clean()  :
  D=doc_dir
  files = glob.glob(D + "/*.json")
  for f in files:
    os.remove(f)

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

def etest() :
  db=get_db('examples/test.txt')
  for ms in materialize(db):
    for m in ms : print(m)
    print('')

def dtest() :
  json_clean()
  #db=get_db('examples/geo.txt')
  #db = get_db('examples/summary.txt')
  db = get_db('examples/test.txt')
  g,pr=to_graph(db)
  gshow(g)

def ttest() :
  fname='examples/texas'
  t = Talker(fname+'.txt')
  #print(t.pr)
  t.show_summary()
  t.show_keywords()
  t.query_with(fname+'_quest.txt')
  #gshow(t.g)

ttest()

#process_docs()
