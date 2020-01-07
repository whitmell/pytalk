annotators=['tokenize','pos','lemma','depparse','ner']+['openie']
openie='openie' in annotators
quiet=True
max_answers=3
trace=1
force=True
from nltk.stem import PorterStemmer
stemmer=PorterStemmer()
#stemmer=None
