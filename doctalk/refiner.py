extractor = None

def refine(text) :
  global extractor
  from summarizer import Summarizer
  if not extractor : extractor=Summarizer()
  return extractor(text)

