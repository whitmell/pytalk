from inspect import getframeinfo, stack
import json

annotators=['tokenize','ssplit','pos','lemma','depparse','ner']+\
           ['natlog','openie']
trace=0

class talk_params:
  def __init__(self,from_dict=None,from_json=None):
    self.force = False

    # content extraction related
    self.compounds = True
    self.svo_edges = True
    self.subject_centered = True
    self.all_to_sent = False
    self.use_to_def = True

    self.pers_idf = False # <========
    self.use_freqs = False
    self.prioritize_compounds = 42


    self.use_line_graph = False # spreads using line_graph

    # 0 : no refiner, just doctalk, but with_bert_qa might control shor snippets
    # 1 : abstractive BERT summarizer, with sumbert postprocessing
    # 2 : extractive BERT summarizer postprocessing
    # 3 : all of the above, concatenated

    self.with_refiner = 0 # <==================
    # controls short answer snippets via bert_qa pipeline
    self.with_bert_qa = 0.000 # <==================

    # summary, and keyphrase set sizes

    self.top_sum = 9 # default number of sentences in summary
    self.top_keys = 10 # # default number of keyphrases

    # maximum values generated when passing sentences to BERT
    self.max_sum = self.top_sum*(self.top_sum-1)/2
    self.max_keys = 1+2*self.top_keys # not used yet

    # query answering related
    self.top_answers = 4 # max number of answers directly shown
    # maximum answer sentences generated when passing them to BERT
    self.max_answers = max(16,self.top_answers*(self.top_answers-1)/2)

    self.cloud_size = 24 # word-cloud size
    self.subgraph_size = 42 # subgraph nodes number upper limit

    self.quiet = True # stops voice synthesis
    self.answers_by_rank = False # returns answers by importance vs. natural order

    self.pers = True # enable personalization of PageRank for QA
    self.expand_query = 2
    self.guess_wh_word_NERs=0 # try to treat wh-word queires as special

    self.think_depth=4

    # visualization / verbosity control

    self.show_pics = 1  # 1 : just generate files, 2: interactive
    self.show_rels = 0  # display relations inferreed from text
    self.to_prolog = 0 # generates Prolog facts

    if from_json:
      jd = json.loads(from_json)
      self.digest_dict(jd)

    if from_dict :
      self.digest_dict(from_dict)

  def digest_dict(self, pydict):
    d = self.__dict__.copy()
    for k, v in d.items():
      if isinstance(k, str) and k in pydict:
        self.__dict__[k] = pydict[k]

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
