annotators=['tokenize','ssplit','pos','lemma','depparse','ner']+\
           ['natlog','openie']
openie='openie' in annotators

sum_count=4
key_count=10
quiet=True
max_answers=5
answers_by_rank=True
trace=1
force=False
from nltk.stem import PorterStemmer
#stemmer=PorterStemmer()
stemmer=None
lower=True
pers=True
expand_query=2
compounds=True
show_pics=1
show_rels=0
to_prolog=1

# decides between '_' and ' ' as separator
def join(*xs) : return '_'.join(xs)

from inspect import currentframe
def ppp(*args) :
  cf = currentframe()
  print('DEBUG at:',cf.f_back.f_lineno,end=': ')
  print(*args)
