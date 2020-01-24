annotators=['tokenize','ssplit','pos','lemma','depparse','ner']+\
           ['natlog','openie']
openie='openie' in annotators

sum_count=4
key_count=10
quiet=True
max_answers=3
answers_by_rank=True
trace=1
force=False
from nltk.stem import PorterStemmer
#stemmer=PorterStemmer()
stemmer=None
lower=True
pers=True
expand_query=1
compounds=True
show=1
def ppp(*args) :
  print('DEBUG:',end='')
  print(*args)
