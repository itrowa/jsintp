
# 根据ply.lex的要求定义javascript的tokens.
# 用于为ply.lex构件一个token分析器.

import ply.lex as lex

tokens = (
        'ANDAND',       # &&
        'COMMA',        # ,
        'DIVIDE',       # /
        'ELSE',         # else
        'EQUAL',        # =
        'EQUALEQUAL',   # ==
        'FALSE',        # false
        'FUNCTION',     # function
        'GE',           # >=
        'GT',           # >
        'IDENTIFIER',   # factorial
        'IF',           # if
        'LBRACE',       # {
        'LE',           # <=
        'LPAREN',       # (
        'LT',           # <
        'MINUS',        # -
        'MOD',          # %
        'NOT',          # !
        'NUMBER',       # 1234 5.678
        'OROR',         # ||
        'PLUS',         # +
        'RBRACE',       # }
        'RETURN',       # return
        'RPAREN',       # )
        'SEMICOLON',    # ;
        'STRING',       # "this is a \"tricky\" string"
        'TIMES',        # *
        'TRUE',         # TRUE
        'VAR',          # var 
        'WHILE',        # while 
) 

# 定义一个comment状态.
states = (
        ('comment', 'exclusive'),    # /* ... */ 
) 

def t_comment(t):
        r'\/\*'                 # /*
        t.lexer.begin('comment') 

def t_comment_end(t): 
        r'\*\/'                 # */
        t.lexer.lineno += t.value.count('\n') 
        t.lexer.begin('INITIAL') 
        pass 

def t_comment_error(t):
        t.lexer.skip(1) 

def t_eolcomment(t):
        r'//.*'                 # 以 //开头的任何字符..
        pass 

# 定义保留字
reserved = [ 'function', 'if', 'var', 'return', 'else', 'true', 'false', 'while' ]

# javascript 的token类型==========================
# 简单的就直接用正则定义; 需要一些进一步处理的token使用函数进行定义:

def t_IDENTIFIER(t):
        r'[A-Za-z][A-Za-z_]*'
        # 如果变量名是保留字, 则此token的类型应该变成对应的type.
        if t.value in reserved:
                t.type = t.value.upper() 
        return t 

# 13
# -13
# 13.
# 13.00001
def t_NUMBER(t):
        r'-?[0-9]+(\.[0-9]*)?' 
        t.value = float(t.value) 
        return t

# string: 
# 必须包含在""内;
# 可以分成两种类型的，一种是非 转义的字符"" 或者 "abc 3j923j)*(&"
# 一种是转义字符，例如"\n \s"
def t_STRING(t):
        r'"([^"\\]|(\\.))*"'
        t.value = t.value[1:-1] # strip off "
        return t

t_ANDAND        = r'&&' 
t_COMMA         = r','
t_DIVIDE        = r'/'
t_EQUALEQUAL    = r'=='
t_EQUAL         = r'='
t_LPAREN        = r'\('
t_LBRACE        = r'{'
t_RBRACE        = r'}'
t_SEMICOLON     = r';'
t_MINUS         = r'-'
t_MOD           = r'%'
t_NOT           = r'!'
t_OROR          = r'\|\|'
t_PLUS          = r'\+'
t_RPAREN        = r'\)'
t_TIMES         = r'\*' 
t_LE            = r'<='
t_LT            = r'<'
t_GT            = r'>'
t_GE            = r'>='

# 在初始状态和comment状态要忽略的东西: 空格, 制表符, carriage return
t_ignore                = ' \t\v\r'
t_comment_ignore        = ' \t\v\r'

def t_newline(t):
        r'\n'
        t.lexer.lineno += 1

def t_error(t):
        print ("JavaScript Lexer: Illegal character " + t.value[0] )
        t.lexer.skip(1) 
