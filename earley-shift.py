# Writing Shift

# We are currently looking at chart[i] and we see x => ab . cd from j. The input is tokens.

# Your procedure, shift, should either return None, at which point there is
# nothing to do or will return a single new parsing state that presumably
# involved shifting over the c if c matches the ith token.

# tokens: a list of tokens
# state: x=> ab . cd from j.
# 函数会返回一条新的state.
def shift (tokens, i, x, ab, cd, j):
    # Insert code here
    if cd != [] and tokens[i] == cd[0]:
        return (x, ab+[cd[0]], cd[1:], j)
    else:
        return None
    

print (shift(["exp","+","exp"],2,"exp",["exp","+"],["exp"],0) == ('exp', ['exp', '+', 'exp'], [], 0))
print (shift(["exp","+","exp"],0,"exp",[],["exp","+","exp"],0) == ('exp', ['exp'], ['+', 'exp'], 0))
print (shift(["exp","+","exp"],3,"exp",["exp","+","exp"],[],0) == None)
print (shift(["exp","+","ANDY LOVES COOKIES"],2,"exp",["exp","+"],["exp"],0) == None)