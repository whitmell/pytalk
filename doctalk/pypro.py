from natlog.natlog import natlog
from natlog.db import db

from .params import *
from .talk import Talker

class NatTalker(Talker) :
  def __init__(self,from_file=None,from_text=None,
               natscript=None,natgoal=None,
               sk=sum_count,wk=key_count,show=show_pics):
    super().__init__(from_file=from_file,from_text=from_text,
        sk=sk,wk=wk,show=show)
    self.natscript=natscript
    self.natgoal=natgoal
    #self.natlog=natlog(text=natscript)

        
  def to_natlog(self):
    nd=db()
    for svo, occs in self.to_svos().items():
      s, v, o = svo
      for id in sorted(occs) :
        c=(s,v,o,id)
        ppp(c)
        nd.add_clause(c)
    return nd

def nrun() :
  natscript = '''

  tc A Rel C : A Rel B, tc1 B Rel C.

  tc1 B _Rel B.
  tc1 B Rel C : tc B Rel C.

  similar A B:
    svo R A Id,
    svo T R B Id.
  '''

  natgoal = 'similar A B?'
