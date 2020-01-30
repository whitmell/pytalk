from natlog.natlog import natlog,Int
from natlog.db import db

from .params import *
from .talk import Talker


class NatTalker(Talker) :
  def __init__(self,from_file=None,from_text=None,
               natscript=None,natgoal=None,
               sk=sum_count,wk=key_count,show=show_pics):
    super().__init__(from_file=from_file,from_text=from_text,
        sk=sk,wk=wk,show=show)
    #self.natscript=natscript
    self.natgoal=natgoal
    self.engine=natlog(text=natscript)
    self.engine.db=self.to_nat_db()

  def to_nat_db(self):
    nd=db()
    for svo, occs in self.to_svos().items():
      s, v, o = svo
      for id in sorted(occs) :
        c=(s,v,o,Int(id)) # should be Int - automatically !!!
        #ppp(c)
        #assert isinstance(id,int)
        nd.add_clause(c)
    return nd

  def natrun(self):
    for answer in self.engine.solve(self.natgoal):
      print('ANSWER:', answer)
      pass

def nrun() :
  natscript = '''

  tc A Rel C : A Rel B, tc1 B Rel C.

  tc1 B _Rel B.
  tc1 B Rel C : tc B Rel C.

  similar A B Id:
    ~ A R B Id,
    T R A Id1,
    T R B Id1.
  '''

  natgoal = 'similar A B Id?'
  #T=Talker(from_file='examples/geo.txt')
  N=NatTalker(from_file='examples/geo.txt',
              natscript=natscript,
              natgoal=natgoal
              )
  N.natrun()

