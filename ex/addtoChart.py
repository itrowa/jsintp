# Addtochart

# Let's code in Python! Write a Python procedure addtochart(chart,index,state)
# that ensures that chart[index] returns a list that contains state exactly
# once. The chart is a Python dictionary and index is a number. addtochart
# should return True if something was actually added, False otherwise. You may
# assume that chart[index] is a list.

# chart: 一个dict. chart[index]: 一个set(用list实现)
# 这个函数将state插入到chart的index处, 如果成功返回True, 如果失败返回False.

def addtochart(chart, index, state):
    # Insert code here!
    if not chart[index]:
        chart[index] = [state]
        return True
    if state in chart[index]:
        return False
    else: 
        chart[index].append(state)
        return True
    