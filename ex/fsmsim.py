# FSM Simulation

edges = {(1, 'a') : 2,
         (2, 'a') : 2,
         (2, '1') : 3,
         (3, '1') : 3}

accepting = [3]

def fsmsim(string, current, edges, accepting):
    """ 判断string是否满足fsm.(能让机器到accepting态.)"""
    if string == "":
        return current in accepting
    else:
        letter = string[0]
        if (current, letter) in edges:   # 如何找到对应的key, 这一句判断的抽象能力太强了.
            destination = edges[(current, letter)]
            return fsmsim(string[1:], destination, edges, accepting)
        else:
            return False
        
#留意, 要递归的元素只有string和current而已.
#@todo: epsilon transition怎么表示.

print (fsmsim("aaa111",1,edges,accepting))
# >>> True