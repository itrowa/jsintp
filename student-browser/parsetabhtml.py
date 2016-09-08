
# D:\Desk-Sync\Github-arsenal\arsenal\CS262\student-browser\parsetabhtml.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '67D196765C6411A86912751487B71A83'
    
_lr_action_items = {'RANGLE':([8,9,11,12,16,19,20,22,23,],[-6,-11,14,-11,-10,-12,-13,24,-7,]),'SLASHRANGLE':([8,9,11,12,16,19,20,],[-6,-11,15,-11,-10,-12,-13,]),'$end':([0,1,2,4,5,6,7,10,15,24,],[-2,-4,0,-3,-2,-5,-14,-1,-8,-9,]),'LANGLESLASH':([1,4,5,6,7,10,14,15,18,24,],[-4,-3,-2,-5,-14,-1,-2,-8,21,-9,]),'EQUAL':([0,1,4,5,6,7,13,14,15,24,],[1,-4,-3,1,-5,-14,17,1,-8,-9,]),'WORD':([0,1,3,4,5,6,7,8,9,12,14,15,17,19,20,21,24,],[4,-4,8,-3,4,-5,-14,-6,13,13,4,-8,19,-12,-13,23,-9,]),'LANGLE':([0,1,4,5,6,7,14,15,24,],[3,-4,-3,3,-5,-14,3,-8,-9,]),'STRING':([0,1,4,5,6,7,14,15,17,24,],[6,-4,-3,6,-5,-14,6,-8,20,-9,]),'JAVASCRIPT':([0,1,4,5,6,7,14,15,24,],[7,-4,-3,7,-5,-14,7,-8,-9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'tag_arguments':([9,12,],[11,16,]),'tagnameend':([21,],[22,]),'tag_argument':([9,12,],[12,12,]),'html':([0,5,14,],[2,10,18,]),'tagname':([3,],[9,]),'element':([0,5,14,],[5,5,5,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> html","S'",1,None,None,None),
  ('html -> element html','html',2,'p_html','htmlgrammar.py',18),
  ('html -> <empty>','html',0,'p_html_empty','htmlgrammar.py',22),
  ('element -> WORD','element',1,'p_element_word','htmlgrammar.py',26),
  ('element -> EQUAL','element',1,'p_element_word_eq','htmlgrammar.py',30),
  ('element -> STRING','element',1,'p_element_word_string','htmlgrammar.py',34),
  ('tagname -> WORD','tagname',1,'p_tagname','htmlgrammar.py',38),
  ('tagnameend -> WORD','tagnameend',1,'p_tagnameend','htmlgrammar.py',44),
  ('element -> LANGLE tagname tag_arguments SLASHRANGLE','element',4,'p_element_tag_empty','htmlgrammar.py',53),
  ('element -> LANGLE tagname tag_arguments RANGLE html LANGLESLASH tagnameend RANGLE','element',8,'p_element_tag','htmlgrammar.py',61),
  ('tag_arguments -> tag_argument tag_arguments','tag_arguments',2,'p_tag_arguments','htmlgrammar.py',67),
  ('tag_arguments -> <empty>','tag_arguments',0,'p_tag_arguments_empty','htmlgrammar.py',71),
  ('tag_argument -> WORD EQUAL WORD','tag_argument',3,'p_tag_argument_word','htmlgrammar.py',75),
  ('tag_argument -> WORD EQUAL STRING','tag_argument',3,'p_tag_argument_string','htmlgrammar.py',79),
  ('element -> JAVASCRIPT','element',1,'p_element_javascript','htmlgrammar.py',83),
]