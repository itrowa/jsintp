#coding:utf-8
import ply.lex as lex
import ply.yacc as yacc
import hjsintp.htmltokens
import hjsintp.htmlgrammar
from hjsintp.htmltokens import *
from hjsintp.htmlgrammar import *



webpage1 = """
<a href="#" class="wrapper"> link_text. </a> 
"""
# [('tag-element', 'a', {'class': 'wrapper', 'href': '#'}, [('word-element', 'link_text.')], 'a')]

webpage2 = """
<script type="text/javascript"> document.write("Hello world!"); </script>
"""
# [('javascript-element', ' document.write("Hello world!"); ')]

webpage3 = """
hello world!
"""
# [('word-element', 'hello'), ('word-element', 'world!')]

webpage4 = """
this is a <b class="em">strong</b> text.
"""

htmllexer = lex.lex(module=hjsintp.htmltokens) 
htmlparser = yacc.yacc(module=hjsintp.htmlgrammar,tabmodule="parsetabhtml") 
ast = htmlparser.parse(webpage4,lexer=htmllexer) 
print(ast)
