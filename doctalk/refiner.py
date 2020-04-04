extractor = None

def refine(doctalk_summary) :
  global extractor
  from summarizer import Summarizer
  from sumbert import summarize
  if not extractor : extractor=Summarizer()
  extractive_bert=extractor(doctalk_summary)
  abstracive_bert=summarize(doctalk_summary)
  d="DOCTALK: "+doctalk_summary
  e="BERT:EXTRACTIVE: "+extractive_bert
  a="BERT:ABSTRACTIVE: "+abstracive_bert
  return "\n".join([d,e,a,"\n"])

