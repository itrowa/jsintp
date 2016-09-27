# -*- coding: utf-8 -*-  
import ply.lex as lex
import ply.yacc as yacc
import htmltokens
import htmlgrammar
import htmlintp
import graphics as graphics # Udacity CS291做的图形库

webpage1 = """
<a href="#" class="wrapper"> link_text. </a> 
"""

# 调用htmltokens定义的tokenizer, 利用lex库生成词法分析器
htmllexer = lex.lex(module=htmltokens) 

# 调用htmlgrammar中定义的CFG, 利用yacc库生成句法分析器. parsing table指定为parsetabhtml
htmlparser = yacc.yacc(module=htmlgrammar,tabmodule="parsetabhtml") 

# 读取输入字符, 生成ast
ast = htmlparser.parse(webpage1,lexer=htmllexer) 


# 初始化绘图库
graphics.initialize() # Enables display of output.

# 调用html解释器解释ast.
htmlintp.interpret(ast) 

# 显示html解释结果.
graphics.finalize() # Enables display of output.