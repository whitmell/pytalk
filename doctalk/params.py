annotators=['tokenize','ssplit','pos','lemma','depparse','ner']+\
           ['natlog','openie']
openie='openie' in annotators

trace=1
force=False

sum_count=4
key_count=10
max_answers=4
cloud_size=24

quiet=True
answers_by_rank=True

from nltk.stem import PorterStemmer
#stemmer=PorterStemmer()
stemmer=None
lower=True
pers=True
expand_query=2

compounds=True
svo_edges=True
subject_centered=True

show_pics=1 # 1 : just generate files, 2: interactive
show_rels=0
to_prolog=1

# decides between '_' and ' ' as separator
#def join(*xs) : return ' '.join(xs)
def join(*xs) : return xs

from inspect import currentframe
def ppp(*args) :
  cf = currentframe()
  print('DEBUG: line-->',cf.f_back.f_lineno,end=': ')
  print(*args)
