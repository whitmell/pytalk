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

    self.prioritize_compounds = 42

    self.use_line_graph = False # spreads using line_graph

    # 0 : no refiner, just doctalk
    # 1 : abstractive BERT summarizer, with sumbert postprocessing
    # 2 : extractive BERT summarizer postprocessing
    # 3 : all of the above, concatenated

    self.with_refiner = 3 # <==================

    # summary, and keyphrase set sizes

    self.top_sum = 9
    self.top_keys = 10

    self.max_sum = self.top_sum*(self.top_sum-1)/2
    self.max_keys = 1+2*self.top_keys

    # query answering related
    self.top_answers = 4
    self.max_answers = max(16,self.top_answers*(self.top_answers-1)/2)

    self.cloud_size = 24
    self.subgraph_size = 32

    self.quiet = True
    self.answers_by_rank = False

    self.pers = True
    self.expand_query = 2
    self.guess_wh_word_NERs=0

    self.think_depth=4

    # visualization / verbosity control

    self.show_pics = 0  # 1 : just generate files, 2: interactive
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
