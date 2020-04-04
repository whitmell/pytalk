# doctalk
Python-based summary and keyword extractor and question answering system with optional BERT-based post-processing filter and spoken output

USAGE:

```
python3 -i

>>> from doctalk.talk import run_with
>>> run_with(fname)
>>> from doctalk.think import reason_with
>>> reason_with(fname)
```
This activates dialog about document in ```<fname>.txt``` with questions in ```<fname>_quests.txt```

See some examples at : 

[https://github.com/ptarau/pytalk](https://github.com/ptarau/pytalk) , where, after installing the system, you can run

```
python3 -i tests.py
>>> go()
>>> tgo()
```
  
To run the system one will need to start the Stanford Corenlp Server, listening on port 9000 with all annotators in params.py started, i.e., with something like:

```
java -mx16g -cp "stanford-corenlp-full-2018-10-05/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 
-preload tokenize,ssplit,pos,lemma,depparse,natlog,openie
```

To play with various parameter settings, edit the ```doctalk/params.py``` file.

Please see the install hints for stanfordnlp, that might involve torch binaries, and require anaconda on some systems.

