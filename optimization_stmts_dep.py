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
        updtated_revstmts = fragment[::-1]

        variables = []              # record all vars
        for stmt in fragment:
            if stmt[0] not in variables:
                variables.append(stmt[0])

        live = []   # recorded live variable
        # keeped = [] # keep all keeped statements
        print("DEBUG - variables: ", variables)
        print("DEBUG - keeped: ", keeped)
        print("DEBUG - revstmts: ", revstmts)
        
        # add returned val into live
        live += returned
        print("DEBUG - live: ", live)

        # reversily treverse all stmt:
        for i, stmt in enumerate(revstmts):         # stmt: ("d", ["c", "b"])
            if stmt == None:
                # 不用删除了;
                # 也不用往live中加入或删除东西了
                pass
            else:
                # keep or del this stmt?
                if stmt[0] not in live:       
                    # keeped.append(stmt)
                    updated_revstmts[i] = None
                print("    DEBUG - revstmts: ", revstmts)

                # update live names
                if stmt[0] in live:
                    live.remove(stmt[0])
                for var in stmt[1]:
                    if var not in live and var in variables:
                        live.append(var)
                print("    DEBUG - live: ", live)
                print("    DEBUG - -next-statement- ")

        revstmts.reverse()            
        return revstmts

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
