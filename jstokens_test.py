import ply.lex as lex
import jstokens             # 导入js 的lex定义

data = """
var x = 32; /* star comment */
// this is a comment

var ceiling_of_5 = function {
    if (x > 5) {
        temp = x;
        return 5;
    }
    else
        return x;
}

"""

# 初始化一个lexer
lexer = lex.lex(module=jstokens)

# 输入一些字符串.
lexer.input(data)

# lex.token() 返回下一个LexToken类型的token实例. 如果遇到字符串末尾则返回None
while 1:
    tok = lex.token()
    if not tok: break
    print (tok)