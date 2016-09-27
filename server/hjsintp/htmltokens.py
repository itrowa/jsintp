# Define a lexer for HTML with embedded Javascript fragments.

import ply.lex as lex

# 定义ply.lex所需要的token names 列表. 这个是必须的.
tokens = (
        'LANGLE',       # < 
        'LANGLESLASH',  # </
        'RANGLE',       # > 
        'SLASHRANGLE',  # /> 
        'EQUAL',        # = 
        'STRING',       # "144" 
        'WORD',         # 'Welcome' in "Welcome to my webpage."
        'JAVASCRIPT',   # embedded JavaScript Fragment
) 
# 通过定义states, 为lex启用带状态的解析规则.
# 默认状态是INITIAL, 现在添加了装个状态: javascript, htmlcomment, 两个状态
# 都是排他性的.
states = (
        ('javascript', 'exclusive'),    # <script type="text/javascript"> 
        ('htmlcomment', 'exclusive'),   # <!-- 
) 

# 每一种token的定义. 根据ply的要求, 定义用t_开头. 传入参数是一个LexToken的实例.

def t_htmlcomment(t): 
        r'<!--' 
        t.lexer.begin('htmlcomment') 

def t_htmlcomment_end(t): 
        r'-->' 
        t.lexer.lineno += t.value.count('\n') 
        t.lexer.begin('INITIAL') 
        pass 

def t_htmlcomment_error(t):
        t.lexer.skip(1) 

def t_javascript(token): 
        r'\<script\ type=\"text\/javascript\"\>' # 等号前后不允许空格.
        token.lexer.code_start = token.lexer.lexpos
        token.lexer.level = 1
        token.lexer.begin('javascript') 

def t_javascript_end(t):
        r'</script>'
        t.value = t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos-9]
        t.type = "JAVASCRIPT"
        t.lexer.lineno += t.value.count('\n') 
        t.lexer.begin('INITIAL') 
        return t 

def t_javascript_error(t):
        t.lexer.skip(1) 

def t_LANGLESLASH(t):
        r'</'
        return t

def t_LANGLE(t):
        r'<' 
        return t

def t_SLASHRANGLE(t):
        r'/>'
        return t

def t_RANGLE(t):
        r'>'
        return t

def t_EQUAL(t):
        r'='
        return t

def t_STRING(t): 
        r'(?:"[^"]*"|\'[^\']*\')'
        t.value = t.value[1:-1] # drop "surrounding quotes" 
        return t

def t_WORD(t):
        r'[^ \t\v\r\n<>=]+' 
        return t

# 在INITLAL, htmlcomment, javascript状态下要忽略的字符.
t_ignore                = ' \t\v\r'
t_htmlcomment_ignore    = ' \t\v\r'
t_javascript_ignore     = ' \t\v\r'

# 默认情况下, 换行符也是文本的一部分, 单我们希望统计换行符出现
# 的次数来作为行号使用.
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1
    
# 定义lex处理非法字符的方式
def t_error(t):
        print ("HTML Lexer: Illegal character " + t.value[0] )
        t.lexer.skip(1) 
