extractor = None

def refine(text) :
  global extractor
  from summarizer import Summarizer
  from sumbert import summarize
  if not extractor : extractor=Summarizer()
  summary=extractor(text)
  absum=summarize(text)
  return summary+"\nIN OTHER WORDS, \n"+absum

def refine1(text) :
  from sumbert import summarize
  absum=summarize(text)
  return absum
