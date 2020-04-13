from .params import talk_params
from .talk import Talker,run_with
from .think import Thinker,reason_with

def new_params(from_json=None) :
  ''' get editable parameter instance,
      use  its show method to list,
      then change any befor using it to make new
      Talker or Thinker
  '''
  return talk_params(from_json=from_json)

def new_talker(from_json=None,params=None) :
  return Talker(from_json=from_json,params=params)

def new_thinker(**kwargs) :
  return Thinker(**kwargs)

def get_summary(talker) :
  return talker.summary_sentences()

def get_keywords(talker) :
  return talker.keywords()

def answer_question(talker,quest) :
  return talker.answer_question(quest)
