# javascript interpreter

# 一些函数定义.
sqrt = ("function",("x"),(("return",("binop",("identifier","x"),"*",("identifier","x"))),),{})

# environment
# env: 一个tuple, 存储着指向父环境的指针; 和一个dict, 存储着name-value的绑定.
# env= (parent, dict)

global_env = (None, { "x": 11,
                      "y": 22,
                      "$write_buffer": "",
                      "sqrt": sqrt,
})

env1 = (global_env, {
    
    "x": 33,
    "z": 44,
})



def env_lookup(name, env):
    """ 查找变量的值. 如果查找不到, 返回None.
    """
    current_env = env[1]
    parent_env = env[0]

    # 先在本地环境查找变量的值; 查找不到, 再去父环境中查找. 
    if name in current_env:
        return current_env[name]
    elif parent_env == None:
        return None
    else:
        return env_lookup(name, parent_env)

def add_binding(name, value, env):
    """ 在当前环境中添加一个name-value的绑定.
    """
    env[1][name] = value

def env_update(name, value, env):
    """ 若变量已存在, 则更新其值
        若变量不存在, 添加一个变量绑定到global frame.
    """
    current_env = env[1]
    parent_env = env[0]

    # 在本地查找到name则更新其值.
    if name in current_env:
        current_env[name] = value
    # 如果这已经是glboal env且查找不到值, 则新增一个绑定.
    elif parent_env == None:
        if not name in current_env:
            current_env[name] = value
    # 往父环境中递归调用自己.
    elif not ((parent_env) == None):
        env_update(name, value, parent_env)



# 在我们的javascript实现中, js的解释结果是一系列字符串, 
# 储存在env的第一帧的"javascript output: "键下.

# 解释器入口 ====================================================

def interpret(ast):
    for elt in ast:
        eval_elt(elt, global_env)
    return (global_env[1])["javascript output"]

def eval_elt(elt, env):
    # help def
    elttype = elt[0]
    eltcontent = elt[1]

    if elttype == 'function':           # function definition?
        pass
    elif elttype == 'stmt':             # statement
        eval_stmt(eltcontent, env)      # stmt@?
    else:
        print ("ERROR - Unknown element " + elt) 

def eval_stmts(stmts, env):
    for stmt in stmts:
        eval_stmt(stmt, env)

def eval_stmt(stmt, env):
    stype = stmt[0]

    # if-then
    # if (<exp>) {...}
    if stype == "if-then":
        predicate = stmt[1]
        consequent = stmt[2] 
        if eval_exp(predicate ,env):
            eval_stmts(consequent, env) 

    # while (<exp>) {}
    elif stype == "while":
        predicate = stmt[1]
        consequent = stmt[2]
        if eval_exp(predicate, env):
            eval_stmts(consequent, env)

    # if (exp) {<stmts>} else {<stmts>}
    # # if x < 5 then A;B; else C;D;
    elif stype == "if-then-else":
        predicate = stmt[1]           
        consequent = stmt[2]
        alternative = stmt[3]
        if eval_exp(predicate, env):
            eval_stmts(consequent, env)
        else:
            eval_stmts(consequent, env)

    # var 变量声明. 
    elif stype == "var":
        varname = stmt[1]
        rhs = stmt[2]
        # 求值rhs的值, 然后在环境中更新
        value_of_rhs = eval_exp(rhs, env)
        add_binding(varname, value_of_rhs, env)


    # x = <exp>
    # eg: ("assign", "x", ("binop", ..., "+",  ...)) <=== x = ... + ...
    elif stype == "assign":
        varname = stmt[1]
        rhs = stmt[2]

        # 求值rhs的exp.
        varval = eval_exp(rhs, env)
        # 在环境中更新varname的值.
        env_update(env, varname, varval)

    elif stype == "return":
        returned = eval_exp(stmt[1], env)
        return returned   # 难道不能这样搞吗

    elif stype == "exp":
        eval_exp(stmt[1], env)

    else:
        print( "ERROR: unknown statement type", stype)

# 求值表达式.
def eval_exp(exp, env):
    etype = exp[0]

    if etype == "identifier":
        varname = exp[1]
        value = env_lookup(varname, env)
        if value == None:
            print("ERROR: unbound variable: " + varname)
        else: 
            return value

    elif etype == "number":
        return float(exp[1])

    elif etype == "string":
        return exp[1]

    elif etype == "true":
        return True

    elif etype == "false":
        return False

    elif etype == "not":
        return not(eval_exp(exp[1], env))

    # 匿名函数对象的声明
    # eg: function(x, y) { return x + y;}
    elif etype == "function":
        # exp: ("function", ["x", "y"], [("return", ("binop", ...)])
        fparams = exp[1]
        fbody = exp[2]
        return ("function", fparams, fbody, env) # 做成闭包.

    # 二元运算
    elif etype == "binop":
        a = eval_exp(exp[1],env)
        op = exp[2]
        b = eval_exp(exp[3],env)
        if op == "+":
                return a+b
        elif op == "-":
                return a-b
        elif op == "/":
                return a/b
        elif op == "*":
                return a*b
        elif op == "%":
                return a%b
        elif op == "==":
                return a==b
        elif op == "<=":
                return a<=b
        elif op == "<":
                return a<b
        elif op == ">=":
                return a>=b
        elif op == ">":
                return a>b
        elif op == "&&":
                return a and b
        elif op == "||":
                return a or b
        else:
                print ("ERROR: unknown binary operator ", op)
                exit(1)

    # call expression / 函数调用
    elif etype == "call":   #("call", "sqrt", [("number", "2")])
        fname = exp[1]                 # 函数名
        args = exp[2]                   # 实际参数的列表

        fvalue = env_lookup(fname, env)  # 取出fname绑定的那个对象.

        if fname == "write":
            argval = eval_exp(args[0], env)
            output_sofar = env_lookup("$write_buffer", env)
            env_update("$write_buffer", output_sofar + str(argval), env)

        if fvalue[0] == "function":  # 如果是一个函数闭包
            # ("function", params, body, env)
            fparams = fvalue[1]
            fbody = fvalue[2]
            fenv = fvalue[3]

            if len(fparams) != len(args):
                print ("ERROR: wrong number of args")
            else:

                # 创建一个新的环境.
                extended_env = (fenv, {})

                # 对每个实参求值, 并在刚刚创建的新环境创建 形式参数 - 实际参数值的绑定.
                for i in range(len(args)):
                    argval = eval_exp(args[i], env)
                    extended_env[1][fparams[i]] = argval

                try:
                    # function body由许多statement组成. 因此用eval_stmts求值.
                    eval_stmts(fbody, extended_env)
                    return None
                except Exception as return_value:
                    return return_value

        # fname在环境中应该绑定到一个闭包上.
        # 如果是闭包, 则求值args,  然后在扩展了的环境中将参数值求值function的body.
        else:
            print ("ERROR: call to non-function ", fname)

    else:
        print ("ERROR: unknown expression type ", etype)











