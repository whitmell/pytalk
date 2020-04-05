import glob
import os
from doctalk.pypro import nrun
from doctalk.talk import *
from doctalk.think import *
from doctalk.vis import *

import pprint

doc_dir="examples/"
doc_files = sorted(glob.glob(doc_dir+"*.txt"))
quest_files = sorted(glob.glob(doc_dir+"*_quest.txt"))

def quest2doc(qf) :
  return qf.replace('_quest.txt','.txt')

#clean files at given directory path
def clean_path(path) :
  os.makedirs(path,exist_ok=True)

  files = glob.glob(path+"/*")
  for f in files:
    os.remove(f)

def clean(force=False)  :
  D=doc_dir
  if force :
    files = glob.glob(D + "/*.json")
    for f in files:
       os.remove(f)
  files = glob.glob(D + "/*_cloud.pdf")
  for f in files:
    os.remove(f)
  files = glob.glob(D + "/*.gv.pdf")
  for f in files:
    os.remove(f)
  files = glob.glob(D + "/*.gv")
  for f in files:
    os.remove(f)
  files = glob.glob(D + "/*.pro")
  for f in files:
    os.remove(f)

# tests to run

def nlp_test() :
  to_json('examples/test.txt', 'examples/temp.json')
  show_extract('examples/test.txt')

def mtest() :
  fname = 'examples/geo.txt'
  t=Talker(from_file=fname)
  db=t.db
  for m in materialize(db) :
    lemmas,words,tags,ners,rels,svos,deps,comps = m
    #pprint.pprint(rels)
    #pprint.pprint(svos)
    pprint.pprint(comps)
    print('')

def otest() :
  fname = 'examples/relativity.txt'
  t=Talker(from_file=fname)
  #rs=t.to_word_orbit('field')
  rs = t.to_sent_orbit(333)
  plot_rank_orbit(rs)

def qtest() :
  fname='examples/geo'
  run_with(fname,query=True,show=True)

def do(qf) :
    df=qf.replace("_quest.txt","")
    run_with(df,query=True)

def qftest() :
  do('examples/const_quest.txt')

def go()  :
  D=doc_dir
  files = sorted(glob.glob(D + "/*_quest.txt"))
  for qf in files:
    df=qf.replace("_quest.txt","")
    run_with(df,query=True)

def ftest() :
  fname='examples/geo'  #################
  run_with(fname,query=False)


def ptest() :
  nrun()

def chat_test() :
  chat_about('examples/bfr')

def canned_test() :
  chat_about('examples/bfr',["What rocket is SpaceX developing?"])

def ttest1() :
  think_test('examples/test.txt','What did Joe give to Mary?')

def ttest2() :
  think_test('examples/geo.txt',
    'What are the source rocks in the Permian Basin ?'
    #'What are the flying pigs fighting lame ducks?'
  )

def think_test(F,Q) :
  T = Thinker(from_file=F)
  T.show_all()
  print('SVO_NODES', T.svo_graph.number_of_nodes())
  print('SVO_EDGES', T.svo_graph.number_of_edges())
  print()
  T.distill(Q)

def tftest():
  fname='examples/hindenburg'  #################
  reason_with(fname,query=True)

def t1() :
    fname = 'examples/bfr'
    reason_with(fname, query=True)


def t2():
  fname = 'examples/hindenburg'
  reason_with(fname, query=True)


def t3():
  fname = 'examples/const'
  reason_with(fname, query=True)

def t4():
  fname = 'examples/logrank'
  reason_with(fname, query=True)

def t5():
  fname = 'examples/heaven'
  reason_with(fname, query=True)

def t6():
  fname = 'examples/einstein'
  reason_with(fname, query=True)

def t7():
  fname = 'examples/geo'
  reason_with(fname, query=True)

def t8():
  fname = 'examples/hindenburg'
  reason_with(fname, query=True)

def t9():
  fname = 'examples/kafka'
  reason_with(fname, query=True)

def t10():
  fname = 'examples/test'
  reason_with(fname, query=True)

def t11():
  fname = 'examples/texas'
  reason_with(fname, query=True)

def t12():
  fname='examples/wasteland'  #################
  reason_with(fname,query=True)

def t13():
  fname='examples/heli'
  reason_with(fname,query=True)

def t14():
  fname='examples/covid'
  reason_with(fname,query=True)

def tgo()  :
  D=doc_dir
  files = sorted(glob.glob(D + "/*_quest.txt"))
  for qf in files:
    df=qf.replace("_quest.txt","")
    reason_with(df,query=True)

if __name__== "__main__" :
  #nlp_test()
  #go()
  #mtest()
  #qftest()
  #simtest()
  #canned_test()
  #ftest()
  #ptest()
  #ttest2()
  #t12()
  #tftest()
  #otest()
  t1()
  pass


