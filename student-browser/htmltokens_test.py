import ply.lex as lex
import htmltokens             # 导入html 的lex定义

webpage1 = """
<a href="#" class="wrapper"> link_text. </a> 
"""

webpage2 = """
<script type="text/javascript"> document.write("Hello world!"); </script>
"""

webpage3 = """
hello world!
"""

# 初始化一个lexer
lexer = lex.lex(module=htmltokens)

# 输入一些字符串.
lexer.input(webpage1)

# lex.token() 返回下一个LexToken类型的token实例. 如果遇到字符串末尾则返回None
while 1:
    tok = lex.token()
    if not tok: break
    print (tok)
