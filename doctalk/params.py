from inspect import getframeinfo, stack

annotators=['tokenize','ssplit','pos','lemma','depparse','ner']+\
           ['natlog','openie']
trace=0

class talk_params:
  def __init__(self):
    self.force = False

    # content extraction related
    self.compounds = True
    self.svo_edges = True
    self.subject_centered = True
    self.all_to_sent = False
    self.use_to_def = True
    self.prioritize_compounds = 100

    self.sum_count = 4
    self.key_count = 6

    # query answering related

    self.max_answers = 3
    self.cloud_size = 24
    self.subgraph_size = 11

    self.quiet = False
    self.answers_by_rank = True

    self.pers = True
    self.expand_query = 2
    self.guess_wh_word_NERs=0

    self.think_depth=4

    # visualization / verbosity control

    self.show_pics = 2  # 1 : just generate files, 2: interactive
    self.show_rels = 0
    self.to_prolog = 0
    


  def __repr__(self):
    return str(self.__dict__)

  def show(self):
    for x,y in self.__dict__.items():
      print(x,'=',y)

def ppp(*args) :
  if trace<0 : return
  caller = getframeinfo(stack()[1][0])

  print('DEBUG:',
        caller.filename.split('/')[-1],
        '->',caller.lineno,end=': ')
  print(*args)
