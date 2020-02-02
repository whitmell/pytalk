from .talk import *

class Thinker(Talker) :
  def __init__(self,**kwargs):
    super().__init__(**kwargs)
    self.svo_graph = self.to_svo_graph()

  def query_with_goal(self, natgoal):
    for answer in distinct(self.engine.solve(natgoal)):
      yield answer
