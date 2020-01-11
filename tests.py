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

def clean()  :
  D=doc_dir
  files = glob.glob(D + "/*.json")
  for f in files:
    os.remove(f)
  files = glob.glob(D + "/*_cloud.pdf")
  for f in files:
    os.remove(f)

def t1() :
  t=Talker(from_text="X gave the book to Mary?")
  gshow(t.g)
  print(t.pr)

def ttest() :
  fname='examples/geo'
  test_with(fname,query=True)



ttest()
#t1()
#process_docs()
