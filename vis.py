from params import show
from graphviz import Digraph as DotGraph
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pathlib import Path

def showGraph(dot, show=True, file_name='textgraph.gv'):
  dot.render(file_name, view=show)

def gshow(g, file_name='textgraph.gv', show=True):
  dot = DotGraph()
  for e in g.edges():
    f, t = e
    # w = g[f][t]['weight']
    w = ''
    dot.edge(str(f), str(t), label=str(w))
  dot.render(file_name, view=show)

def pshow(t, k=24,file_name="cloud.pdf",show=show):
  sum, kws = t.extract_content(5, k)
  d = {w: t.pr[w] for w in kws}
  show_ranks(d,file_name=file_name,show=show)

def show_ranks(rank_dict,file_name="cloud.pdf",show=show) :
  cloud=WordCloud(width=800,height=400)
  cloud.fit_words(rank_dict)
  f=plt.figure()
  plt.imshow(cloud, interpolation='bilinear')
  plt.axis("off")
  if show : plt.show()
  '''
  if exists_file(file_name) :
    for i in range(6):
      fname = file_name.replace("quest_cloud","quest_cloud"+str(i))
      if not exists_file(fname) :
        file_name=fname
        break
  '''
  f.savefig(file_name,bbox_inches='tight')

if __name__=="__main__":
  d = {'a': 0.1, 'b': 0.2, 'c': 0.33, 'd': 0.2}
  show_ranks(d)
