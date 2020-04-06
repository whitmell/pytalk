extractor = None

BERT_ABS=1
BERT_EX=2
ALL=3

def refine(doctalk_summary,how) :
  global extractor
  if how in {BERT_EX,ALL} :
    from summarizer import Summarizer
    if not extractor : extractor=Summarizer()
    extractive_bert=extractor(doctalk_summary)
    if how==BERT_EX :
      return extractive_bert
  if how in {BERT_ABS,ALL} :
    from sumbert import summarize
    abstractive_bert=summarize(doctalk_summary)
    if how == BERT_ABS:
      return abstractive_bert
  if how == ALL:
    e="BERT:EXTRACTIVE: "+extractive_bert
    a="BERT:ABSTRACTIVE: "+abstractive_bert+"."
    return "\n".join([e,a,"\n"])

