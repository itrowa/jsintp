# Earlay Parser

# #################################################
# Grammar, Rule, Token

# grammar = [
#     ("T", ["a", "B", "c"]),
#     ("B", ["b", "b"])
# ]
# start_rule = grammar[0]
# tokens = ["a", "b", "b", "c"]

# # 一条rule 就是一个类似这样的
# ("P", ["(" , "P", ")" ])

# from earley_test import grammar, start_rule, tokens

# 关于Rule, token的各种辅助函数
def lhs_of_rule(rule):
    return rule[0]
def rhs_of_rule(rule):
    return rule[1]

def is_terminal(token, grammar):
    """ is this token a terminal in grammar? """
    for rule in grammar:
        if token == lhs_of_rule(rule):
            return True
    return False    

def is_nonterminal(token, grammar):
    """ is this token a non-terminal in grammar? """
    is_valid_token = False
    for rule in grammar:
        if token in rhs_of_rule(rule):
            is_valid_token = True
            break
    # token必须在grammar中定义; 且token不能在LHS中出现.
    return not is_terminal(token, grammar) and is_valid_token

# ##################################################
# Earley State: 

# 形如: x -> ab * cd at j
# 用python的tuple来表示: state = ("x", ["a", "b"], ["c", "d"], j)

## 选择earley state的各个部分
def lhs_of_state(earley_state):
    return earley_state[0]
def before_dot(earley_state):
    return earley_state[1]
def after_dot(earley_state):
    return earley_state[2]
def from_pos(earley_state):
    return earley_state[3]
def next_token(earley_state):
    if after_dot(earley_state) == []:   return None
    else:                               return (earley_state[2])[0]
def state_repr(earley_state):
    s = ""
    s += lhs_of_state(earley_state) + " -> "
    for sym in before_dot(earley_state):
        s += " " + sym
    s += " . "
    for sym in after_dot(earley_state):
        s += " " + sym
    s += " from " + str(from_pos(earley_state)) + " "
    return s


def build_chart(grammar, tokens):
    """通过grammar和输入的token建立Earley Chart并返回.
    """
    chart = {}
    for i in range(len(tokens) + 1):
        chart[i] = []

    # 将初始化规则放入chart中    
    start_state = (lhs_of_rule(start_rule), [], rhs_of_rule(start_rule), 0)
    chart[0].append (start_state)
    # print("DEBUG - Init chart: ")
    # print_chart(chart)

    for i in chart: # i 分别取chart中每个key, 作为下标使用.
        state_set = chart[i]
        # print("DEBUG - filling chart{0:1d}".format(i))
        for state in state_set:  # 取出当前state set的每一个state
            # print("    DEBUG - current state: ", state_repr(state))
            next_t = next_token(state)
            # print("    DEBUG - next token: ", next_t)


            if is_terminal(next_t, grammar):
                # print("    DEBUG - go for case 1.. ")
                predict(grammar, i, chart, next_t)
            elif is_nonterminal(next_t, grammar):
                next_input = tokens[i]
                if next_input == next_t:    # 如果下一个输入的token等于这条state中下一个token
                    # print("    DEBUG - go for case 2.. ")
                    shift(state, i, chart)
            elif next_t == None:
                # print("    DEBUG - go for case 3.. ")
                reduction(state, i, chart)
            else: 
                # print("Undefined token", next_token)
                break
            # print("    DEBUG - gen for this state over. now chart is: ")
            # print_chart(chart)
        # print("    DEBUG - gen for this state set over. now chart is: ")
        # print_chart(chart)
                
    return chart

def predict(grammar, i, chart, token):
    """ 在grammar中寻找是否有lhs 等于 token的规则. 如果有, 把这些规则编辑成state的列表, 每一个state有如下的形式:
        token -> . p q r (i)
        然后把state列表加入chart[i]
    """
    for rule in grammar:
        if lhs_of_rule(rule) == token:
            predicted_state = (lhs_of_rule(rule),
                               [],
                               rhs_of_rule(rule), 
                               i)
            add_to_chart(chart, i, predicted_state)
            # print("DEBUG-PREDICT - insert " + state_repr(predicted_state) + "to chart[" + str(i) + "]..")

def shift(state, i, chart):
    """ state: x -> a b . c d (j)
        new:   x -> a b c . d (j)
        然后加入到chart[i+1]中.
    """
    # print("DEBUG-SHIFT - state", state)
    new_state = (lhs_of_state(state),                              # lhs
                 before_dot(state) + [after_dot(state)[0]],        # before_dot part
                 after_dot(state)[1:],                             # after_dot part
                 from_pos(state))                                  # from position
    add_to_chart(chart, i+1, new_state)
    # print("DEBUG-SHIFT - insert " + state_repr(new_state) + "to chart[" + str(i+1) + "]..")

def reduction(state, i, chart):
    """ 对于在chart[i]处的state: x -> e f g . (j)
        在chart[j]中寻找是否有next_token就是 x的state (例如: z -> l . x y (j)). 如果有, 则改写这条rule为
        z -> l x . y (j) 并添加到chart[i].
    """ 
    for formal_state in chart[from_pos(state)]:  # state的from_position处为j, 那么去chart[j] 取出各个state
        # print("    DEBUG-REDUCTION - formal_state", formal_state)
        # print("    DEBUG-REDUCTION - next_token: ", next_token(formal_state))
        if next_token(formal_state) == None:
            break
        else:
            if next_token(formal_state) == lhs_of_state(state):   # 如果state的next_tokoen 等于state的lhs的话

                reduction_state = (lhs_of_state(formal_state), 
                                   before_dot(formal_state) + [after_dot(formal_state)[0]], 
                                   after_dot(formal_state)[1:],
                                   from_pos(formal_state)
                                   )
                add_to_chart(chart, i, reduction_state)
                # print("DEBUG-REDUCTION - insert " + state_repr(reduction_state) + "to chart[" + str(i) + "]..")



def add_to_chart(chart, index, state):
    """ 将state 插入到chart[index]处. 前提是, chart[index]中这个state并不存在.
    """
    state_set = chart[index]
    if not(state in state_set):
        state_set.append(state)

def print_chart(chart):
    for i in chart:
        print ("== chart " + str(i) + ": ")
        state_set = chart[i] # a list of states.

        for state in state_set:
            print ("   " + lhs_of_state(state) + " ->", end="")
            for token in before_dot(state) :
                print (" " + token, end="")
            print( " .", end="")
            for token in after_dot(state):
                print (" " + token, end="")
            print (" from " + str(from_pos(state)))

def diagnose(input, grammar, chart):
    """ 对于输入的tokens, 和预定义的语法集, 和已建立好的Earley state表而言,
        这个input是不是属于此语言?
    """
    accepting_state = (lhs_of_rule(start_rule), rhs_of_rule(start_rule), [], 0)
    return accepting_state in chart[len(chart)-1] # 如果accepting_state在chart的最后一个element中. 则parse成功.


grammar = [
    ("T", ["a", "B", "c"]),
    ("B", ["b", "b"])
]
start_rule = grammar[0]
tokens = ["a", "b", "b", "c"]

print("building chart....")
c = build_chart(grammar, tokens)
print("\nbuilding chart complete. chart is: \n")
print_chart(c)
print("\ninput is in this grammar? " + str(diagnose(tokens, grammar, c)))
