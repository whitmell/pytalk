from inspect import getframeinfo, stack

annotators=['tokenize','ssplit','pos','lemma','depparse','ner']+\
           ['natlog','openie']

class talk_params:
  def __init__(self):
    self.trace = 1
    self.force = False

    self.sum_count = 4
    self.key_count = 10
    self.max_answers = 4
    self.cloud_size = 24
    self.subgraph_size = 32

    self.quiet = True
    self.answers_by_rank = True

    self.lower = True
    self.pers = True
    self.expand_query = 2

    self.compounds = True
    self.svo_edges = True
    self.subject_centered = True

    self.show_pics = 1  # 1 : just generate files, 2: interactive
    self.show_rels = 0
    self.to_prolog = 0

params=talk_params()

# decides between '_' and ' ' as separator
#def join(*xs) : return ' '.join(xs)
def join(*xs) : return xs

def ppp(*args) :
  caller = getframeinfo(stack()[1][0])

  print('DEBUG!!!',
        caller.filename.split('/')[-1],
        '->',caller.lineno,end=': ')
  print(*args)
