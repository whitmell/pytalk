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
    self.params.max_answers,to_show=20,5
    answers,answerer=self.answer_quest(q)
    show_answers(self,take(to_show,answers))
    self.reason_about(answers,answerer)

  def walks(self,lemmas,g):
    lemmas=list(lemmas)
    paths=[]
    l = len(lemmas)
    for i in range(l) :
      for j in range(i) :
        p=chain(g,lemmas[i],lemmas[j])
        if p: paths.extend(p)
    return paths

  def add_rel(self,ps):
    p=ps.pop()



  def reason_about(self,answers,answerer):
    rels= (
      'as_in','is_like','kind_of', 'part_of','has_instance'
      'subject_in', 'object_in', 'verb_in')
    no_rels=() #('object_in', 'verb_in','kind_of')

    lemmas = answerer.get_lemma(0)
    tags=answerer.get_tag(0)
    lts=zip(lemmas,tags)
    good_lemmas={l for (l,t) in lts if good_word(l) and good_tag(t)}

    ppp("GOOD_LEMMAS",len(good_lemmas),sorted(good_lemmas))
    G=self.svo_graph
    depth=16
    xs=reach_from(G,depth,lemmas)
    ppp(xs)
    print('')

    ys = reach_from(G.reverse(copy=False),
                    depth, lemmas, reverse=True)
    ppp(ys)

    '''
    paths = self.walks(good_lemmas,self.svo_graph)
    ppp(len(paths),sorted(paths))
    roots={p for ps in paths for p in ps}

    if self.params.guess_wh_word_NERs :
      roots.update(extend_wh(lemmas))

    ppp('ROOTS:',len(roots),sorted(roots))


    U=self.svo_graph
    #U = as_undir(U)
    #U = with_rels(U, rels)
    #U = without_rels(U,no_rels)
    reached=set()
    for l in roots :
      if l in U.nodes() :
        reached.update(near_in(U,l))
    reached.update(roots)

    tprint('TOTAL REACHED',len(reached))
    S=U.subgraph(reached)
    #for x in S : ppp(x)
    '''
    good_nodes={a for x in xs.union(ys) for a in x}
    S=G.subgraph(good_nodes)
    self.show_svo_graph(S)


def reach_from(g,k,roots,reverse=False):
    edges=set()
    for x in roots :
      if not x in g.nodes() : continue
      xs = nx.dfs_edges(g,x,depth_limit=k)
      for e in xs :
        a,b=e
        if b in roots :
          rel=g[a][b]['rel']
          edge= (b,rel,a) if reverse  else  (a,rel,b)
          edges.add((a,rel,b))
    return edges

def chain(g, here, there):
    try:
      p = list(nx.all_shortest_paths(g, here, there,method='bellman-ford'))
    except :
      p = []
    return p

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
