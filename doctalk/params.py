annotators=['tokenize','ssplit','pos','lemma','depparse','ner']+\
           ['natlog','openie']
openie='openie' in annotators

trace=1
force=False

sum_count=4
key_count=10
max_answers=4
cloud_size=24
subgraph_size=32

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
to_prolog=0

# decides between '_' and ' ' as separator
#def join(*xs) : return ' '.join(xs)
def join(*xs) : return xs


from inspect import getframeinfo, stack

def ppp(*args) :
  caller = getframeinfo(stack()[1][0])

  print('DEBUG!!!',
        caller.filename.split('/')[-1],
        '->',caller.lineno,end=': ')
  print(*args)
