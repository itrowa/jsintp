from jsintp import *

test_tree1 = ("binop",("number","5"),"+",("number","8"))
# print eval_exp(test_tree1) == 13

test_tree2 = ("number","1776")
# print eval_exp(test_tree2) == 1776

test_tree3 = ("binop",("number","5"),"+",("binop",("number","7"),"-",("number","18")))
# print eval_exp(test_tree3) == -6


print (eval_exp(("call","sqrt",[("number","2")]), global_env))

# if-then-else测试
if__then_else_ast = ("if-then-else", ("true", "true"), ("assign", "x", ("number", "8")), ("assign", "x", "5"))
eval_stmts(tree, environment)