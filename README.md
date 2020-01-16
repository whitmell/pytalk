# doctalk
Simple Python-based query  answering system with optional voice output

USAGE:

```
python3 -i

>>> from doctalk import run_with
>>> run_with(fname)
```
This ctivates dialog about document in ```<fname>.txt``` with questions in ```<fname>_quests.txt```
  
It assumes Stanford Corenlp Server listening on port 9000 with all annotators in params.py started with something like:

```
java -mx16g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 
-preload tokenize,ssplit,pos,lemma,depparse,natlog,openie
```

See some examples at : https://github.com/ptarau/pytalk .

Please see the install hints for stanfordnlp, that might involve torch binaries, and require anaconda on some systems.

