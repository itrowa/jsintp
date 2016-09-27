#coding:utf-8
import ply.lex as lex
import ply.yacc as yacc
import jstokens
import jsgrammar



jscript1 = """
var a = 5;
var b = 2;
/* star comment */
// line comment
"""
# [('stmt', ('var', 'a', ('number', 5.0))), ('stmt', ('var', 'b', ('number', 2.0)))]

jscript2 = """
var x = 32; /* star comment */
// this is a comment

var ceiling_of_5 = function() {
    if (x > 5) {
        temp = x;
        return 5;
    }
    else
        return x;
};
"""
# [('stmt', ('var', 'x', ('number', 32.0))), ('stmt', ('var', 'ceiling_of_5', ('function', [], [('if-then-else', ('binop', ('identifier', 'x'), '>', ('number', 5.0)), [('assign', 'temp', ('identifier', 'x')), ('return', ('number', 5.0))], [('return', ('identifier', 'x'))])])))]

jslexer = lex.lex(module = jstokens) 
jsparser = yacc.yacc(module = jsgrammar, tabmodule = "parsetabjs") 
ast = jsparser.parse(jscript2, lexer = jslexer) 
print(ast)