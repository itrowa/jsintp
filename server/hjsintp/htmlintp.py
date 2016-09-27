# the HTML interpreter.
# only handles a subset of html.

import graphics as graphics # Udacity CS291做的图形库

def interpret(ast):
    for node in ast:
        nodetype = node[0]

        if nodetype == "word-element":
            # eg: ("word-element", "hello")
            graphics.word(node[1])
        elif nodetype == "tag-element":
            # eg: <b class="info"> strong text! </b>
            tagname = node[1]   # b
            tagargs = node[2]   # {"class": "info"}
            subast = node[3]    # ... Strong text!
            closetagname = node[4] # b

            if tagname != closetagname:
                graphics.warning("(mismatched " + tagname + " " + closetagname + ")")
            else:
                graphics.begintag(tagname, tagargs)
                interpret(subast) # 递归解释标签内的html内容.
                graphics.endtag()
        elif nodetype == "javascript-element":
            jstext = node[1]
            pass
            # 未完工; 取出jstext后应该调用javascript解释器去解释这个东西.

# test
html = """
hello my
<script type = "text/javascript"> document.write(99); </script>
loft ballons
"""

ast = [
  ("word-element", "hello"),
  ("word-element", "my"),
  ("javascript-element", "document.write(99);"),
  ("word-element", "loft ballons"),
]