# Living statement: the value that holds my be needed in the future.
# formally we say a variable is live at some point P if it may be read
# before being overwritten after P. 


# live: 这个变量是不是live的, 是相对于某一行而言的.
# 在某一行处, 这个变量被overwrite前 它会被读取. 我们就说这个variable相对于这一行而言, 是live的.
# 

# We will encode JavaScript fragments as lists of tuples. For example,
#
#               a = 1;
#               b = a + 1;
#               c = 2;
#
# Will be encoded as:
#
fragment2 = [ ("a", ["1"] ) ,           # a = 1
              ("b", ["a", "1"] ),       # b = a operation 1
              ("c", ["2"] ), ]          # c = 2 


def removedead(fragment,returned): 
        # fill in your answer here (can be done in about a dozen lines)
        old_frag = fragment
        new_frag = []
        live = returned

        for stmt in fragment[::-1]:   # 反向遍历fragment的每一个stmt.
            # stmt: ("b", ["a", "1"]) 这样的

            # 如果LHS的变量名已经在live中了 我们就保留它?
            if stmt[0] in live:
                new_frag = [stmt] + new_frag

            # 更新live中记录的变量.
            live = [var for var in live if var != stmt[0]]
            live = live + stmt[1]

        if new_frag == old_frag:
            return new_frag
        else:
            return removedead(new_frag, returned)

# We have provided a few test cases. You may want to write your own.

fragment1 = [ ("a", ["1"]), 
              ("b", ["2"]), 
              ("c", ["3"]), 
              ("d", ["4"]), 
              ("a", ["5"]), 
              ("d", ["c","b"]), ]

print (removedead(fragment1, ["a","d"]))

print (removedead(fragment2, ["c"]))

print (removedead(fragment1, ["a"]))

print (removedead(fragment1, ["d"]))
