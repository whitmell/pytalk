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
    abstracive_bert=summarize(doctalk_summary)
    if how == BERT_ABS:
      return abstracive_bert
  if how == ALL:
    d="DOCTALK: "+doctalk_summary
    e="BERT:EXTRACTIVE: "+extractive_bert
    a="BERT:ABSTRACTIVE: "+abstracive_bert
    return "\n".join([d,e,a,"\n"])

