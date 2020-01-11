import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

d={'a':0.1,'b':0.2,'c':0.33,'d':0.2}
def show_ranks(rank_dict) :
  cloud=WordCloud()
  cloud.fit_words(rank_dict)
  plt.imshow(cloud, interpolation='bilinear')
  plt.axis("off")
  plt.show()

#show_ranks(d)
