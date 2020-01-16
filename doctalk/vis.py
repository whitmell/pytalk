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

def pshow(t, k=24,file_name="temp",show=show):
  def t2s(x) :
    if isinstance(x,tuple) :
      return " ".join(x)
    return x
  sum, kws = t.extract_content(5, k)
  #ppp(t.by_rank)
  d0 = {w: t.pr[w] for w in kws}
  d={t2s(w) : t.pr[w] for w in d0}
  #ppp("DDDD",d0)
  show_ranks(d,file_name=file_name+"_cloud.pdf",show=show)
  topg=t.g.subgraph(d0)
  gshow(topg,file_name+".gv",show=show)

def show_ranks(rank_dict,file_name="cloud.pdf",show=show) :
  cloud=WordCloud(width=800,height=400)
  cloud.fit_words(rank_dict)
  f=plt.figure()
  plt.imshow(cloud, interpolation='bilinear')
  plt.axis("off")
  if show>1 : plt.show()
  f.savefig(file_name,bbox_inches='tight')

if __name__=="__main__":
  d = {'a': 0.1, 'b': 0.2, 'c': 0.33, 'd': 0.2}
  show_ranks(d)
