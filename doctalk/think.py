from .talk import *

def extend_wh(lemmas) :
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
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    self.svo_graph = self.to_svo_graph()

  def ask(self,q):
    print('QUESTION:',q,'\n')
    answers,answerer=self.answer_quest(q,max_answers=25)
    #show_answers(take(3,answers))
    lemmas=answerer.get_lemma(0)
    ids = dict()
    shareds = set()
    ppp('LEMMAS:',lemmas)
    if 'who' in lemmas :
      shareds.update({'person','title','organization'})
    if 'when' in lemmas :
      shareds.update({'time','duration','date'})
    if 'where' in lemmas :
      shareds.update({'location','organization','city','state_or_province','country'})
    if 'how' in lemmas and ('much' in lemmas or 'many' in lemmas) :
      shareds.update({'money','number','ordinal'})
    for answer in answers:
       id, sent,rank,shared=answer
       ids[id]=rank
       shareds.update(shared)
    rels= (
      'as_in','is_like',
       'is_a', 'part_of',
      'is_kind_of'
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
    ppp('LEN',len(reached))

    S=U.subgraph(reached)
    show_svo_graph(S, size=42,show=2)

def near_in(g,x) :
  xs1=nx.neighbors(g,x)
  return xs1
  xs2=set(y for x in xs1 for y in nx.neighbors(g,x))
  return xs2.union(xs1)

def as_undir(g) : return g.to_undirected(as_view=True)

def with_rels(G,rels) :
  return nx.subgraph_view(G,
    filter_edge=lambda x,y:G[x][y]['rel'] in rels )

def without_rels(G,rels) :
  return nx.subgraph_view(G,
    filter_edge=lambda x,y:G[x][y]['rel'] not in rels )
