from .talk import *

def extend_wh(lemmas) :
  ''' ads possible NER targets for wh words'''
  xs=set()
  if 'who' in  lemmas:
    xs.update({'person', 'title', 'organization'})
  if 'when' in lemmas:
    xs.update({'time', 'duration', 'date'})
  if 'where' in lemmas:
    xs.update({'location', 'organization', 'city', 'state_or_province', 'country'})
  if 'how' in lemmas and ('much' in lemmas or 'many' in lemmas):
    xs.update({'money', 'number', 'ordinal'})
  if 'what' in lemmas and 'time' in lemmas:
    xs.update({'time', 'duration', 'date'})
  return xs

class Thinker(Talker) :
  '''
  extends Talker with multi-hop resoning over SVOs
  using graph algorithms
  '''
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    self.svo_graph = self.to_svo_graph()

  def ask(self,q):
    ''' handler for question q asked from this Thinker'''
    print('QUESTION:',q,'\n')
    answers,answerer=self.answer_quest(q)
    show_answers(take(4,answers))
    self.reason_about(answers,answerer)

  def reason_about(self,answers,answerer):
    lemmas = answerer.get_lemma(0)
    tprint('LEMMAS:', lemmas)
    ids = dict()
    shareds = extend_wh(lemmas)

    for answer in answers:
       id, sent,rank,shared=answer
       ids[id]=rank
       shareds.update(shared)
    rels= (
      'as_in','is_like',
       'is_a', 'part_of',
      'has_instance'
      'subject_in', 'object_in', 'verb_in'
    )
    no_rels=('object_in', 'verb_in','is_a'
     )
    tprint('SHAREDS',shareds)
    U=self.svo_graph
    U = as_undir(U)
    #U = with_rels(U, rels)
    U = without_rels(U,no_rels)
    reached=set()
    for sh in shareds :
      if sh in U.nodes() :
        reached.update(near_in(U,sh))
    reached.update(shareds)
    tprint('TOTAL REACHED',len(reached))

    S=U.subgraph(reached)
    self.show_svo_graph(S)

def near_in(g,x) :
  '''
  returns all 1 or 2 level neighbors of x in g
  '''
  xs1=nx.neighbors(g,x)
  return xs1
  xs2=set(y for x in xs1 for y in nx.neighbors(g,x))
  return xs2.union(xs1)

def as_undir(g) :
  '''view of g as an undirected graph'''
  return g.to_undirected(as_view=True)

def with_rels(G,rels) :
  ''''view of G that follows only links in rels'''
  return nx.subgraph_view(G,
    filter_edge=lambda x,y:G[x][y]['rel'] in rels )

def without_rels(G,rels) :
  ''''view of G that follows only links NOT in rels'''
  return nx.subgraph_view(G,
    filter_edge=lambda x,y:G[x][y]['rel'] not in rels )
