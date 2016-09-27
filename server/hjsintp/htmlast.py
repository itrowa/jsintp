#coding:utf-8
import ply.lex as lex
import ply.yacc as yacc
import hjsintp.htmltokens
import hjsintp.htmlgrammar

def parseHtml(text):
    """ for a given text return ast. 
    """
    htmllexer = lex.lex(module=hjsintp.htmltokens) 
    htmlparser = yacc.yacc(module=hjsintp.htmlgrammar,tabmodule="parsetabhtml") 
    return htmlparser.parse(text, lexer=htmllexer) 