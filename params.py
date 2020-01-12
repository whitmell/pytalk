annotators=['tokenize','ssplit','pos','lemma','depparse','ner']+['natlog','openie']
openie='openie' in annotators
quiet=True
max_answers=5
trace=1
force=False
from nltk.stem import PorterStemmer
#stemmer=PorterStemmer()
stemmer=None
lower=True
pers=True
show=True
def ppp(*args) :
  print('DEBUG:',end='')
  print(*args)
