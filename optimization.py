# optimization example
# 对于一个给定的AST 在不改变其sematics(meaning)的情况下改变其AST的结构(简化其结构). 
# 当然简化的规则目前还比较简单. 仅仅是对二元运算的一些特殊情况作出优化.

def optimize(tree):
    etype = tree[0]

    # 如果AST属于二元数运算:
    if etype == 'binop':            
        # a * 1  --> a
        a = optimize(tree[1])
        op = tree[2]
        b = optimize(tree[3])
        if op == "*" and b == ("number", "1"):
            return a 
        elif op == "*" and b == ("number", "0"):
            return ("number", "0")
        elif op == "+" and b == ("number", "0"):
            return a
        else: # tree不满足优化的任何一个条件
            return tree

        # arithmetic laws

        # number * 0 -> 0
        if op == "*" and (a == ("number", 0) or b == ("number", 0)):
            return ("number", 0)

        # number * 1 -> number
        elif op == "*" and a == ("number", 1):
            return b
        elif op == "*" and b == ("number", 1):
            return a

        # number + 0 -> number
        elif op == "+" and a == ("number", 0):
            return b
        elif op == "+" and b == ("number", 0):
            return a

        # constant - same constant -> 0
        elif op == "-" and a == b:
            return ("number", 0)

        # constant folding:
        if a[0] == "number" andb[0] == "number":
            if op == "+":
                return ("number", a[1] + b[1])
            elif op == "-":
                return ("number", a[1] - b[1])
            elif op == "*":
                return ("number", a[1] * b[1])

        else:
            return ("binop", a, op, b)

    else:
        return tree


# (a * 1)
print (optimize(("binop",("number","5"),"*",("number","1"))) == ("number","5"))
print (optimize(("binop",("number","5"),"*",("number","0"))) == ("number","0"))
print (optimize(("binop",("number","5"),"+",("number","0"))) == ("number","5"))

# a + ( 5 * 0)   = a + 0  = a
print (optimize(("binop",("number","5"),"+",("binop",("number","5"),"*",("number","0")))) == ("number","5"))
