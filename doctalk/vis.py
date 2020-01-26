from .params import *
from graphviz import Digraph as DotGraph
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def showGraph(dot, show=True, file_name='textgraph.gv'):
  dot.render(file_name, view=show)

def gshow(g, file_name='temp.gv', show=1):
  dot = DotGraph()
  for e in g.edges():
    f, t = e
    # w = g[f][t]['weight']
    w = ''
    dot.edge(str(f), str(t), label=str(w))
  dot.render(file_name, view=show>1)

def pshow(t, k=24,file_name="temp",show=show_pics):
  def t2s(x) :
    if isinstance(x,tuple) :
      return " ".join(x)
    return x
  sum, kws = t.extract_content(5, k)
  #ppp(t.by_rank)
  d=dict()
  s=set()
  for kw in kws:
    if isinstance(kw,tuple) :
      kw0=tuple(map(lambda x: x.lower(),kw))
      d[t2s(kw)]=t.pr[kw0]
      s.add(kw0)
    else :
      d[kw]=t.pr[kw.lower()]
      s.add(kw)
  #ppp("DDDD",d)
  show_ranks(d,file_name=file_name+"_cloud.pdf",show=show)
  topg=t.g.subgraph(s)
  gshow(topg,file_name+".gv",show=show)

def show_ranks(rank_dict,file_name="cloud.pdf",show=show_pics) :
  cloud=WordCloud(width=800,height=400)
  cloud.fit_words(rank_dict)
  f=plt.figure()
  plt.imshow(cloud, interpolation='bilinear')
  plt.axis("off")
  if show>1 : plt.show()
  f.savefig(file_name,bbox_inches='tight')
  plt.close('all')

if __name__=="__main__":
  d = {'a': 0.1, 'b': 0.2, 'c': 0.33, 'd': 0.2}
  show_ranks(d)
