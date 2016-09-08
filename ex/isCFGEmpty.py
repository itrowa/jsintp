# problem set 3 Reading Machine Minds 2
# 一套CFG指定的语言是空吗? (对于给定的语法集grammar和一个符号symbol, 能重写出最终结果吗?) 如果是空返回None, 如果不是, 返回其中一个重写结果.
def cfgempty(grammar, symbol, visited):
    if symbol in visited:
        # 进入循环, 意味着无法接受有限的字符串. 因此返回None
        return None
    elif not any([rule[0] === symbol for rule in grammar]):
        # base case: 'symbol'是terminal
        return [symbol]
    else:
        new_visited = visited + [symbol]
        for rhs in [r[1]] for r in grammar if r[0] == symbol]:  # for every RHS result that match Symbol-> RHS
            if all([None != cfgempty(grammar, r, new_visited) for r in rhs]): # 对于这个RHS中所有的symbol, 都能进行重写, 那么...
                # gather up result
                result = []
                for r in rhs:
                    result = result + cfgempty(grammar, r, new_visited)
                return result
        # didn't find any
        return None