
# parsetabhtml.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '67D196765C6411A86912751487B71A83'
    
_lr_action_items = {'EQUAL':([0,1,3,4,5,6,11,16,17,24,],[4,-3,4,-4,-5,-14,14,4,-8,-9,]),'WORD':([0,1,3,4,5,6,7,9,10,12,14,16,17,18,19,21,24,],[1,-3,1,-4,-5,-14,9,-6,11,11,18,1,-8,-12,-13,23,-9,]),'JAVASCRIPT':([0,1,3,4,5,6,16,17,24,],[6,-3,6,-4,-5,-14,6,-8,-9,]),'LANGLE':([0,1,3,4,5,6,16,17,24,],[7,-3,7,-4,-5,-14,7,-8,-9,]),'RANGLE':([9,10,12,13,15,18,19,22,23,],[-6,-11,-11,16,-10,-12,-13,24,-7,]),'LANGLESLASH':([1,3,4,5,6,8,16,17,20,24,],[-3,-2,-4,-5,-14,-1,-2,-8,21,-9,]),'$end':([0,1,2,3,4,5,6,8,17,24,],[-2,-3,0,-2,-4,-5,-14,-1,-8,-9,]),'STRING':([0,1,3,4,5,6,14,16,17,24,],[5,-3,5,-4,-5,-14,19,5,-8,-9,]),'SLASHRANGLE':([9,10,12,13,15,18,19,],[-6,-11,-11,17,-10,-12,-13,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'tagnameend':([21,],[22,]),'element':([0,3,16,],[3,3,3,]),'tag_argument':([10,12,],[12,12,]),'tagname':([7,],[10,]),'html':([0,3,16,],[2,8,20,]),'tag_arguments':([10,12,],[13,15,]),}

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