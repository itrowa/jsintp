from earley import *

# the grammar by loup-vaillant.fr
# grammar = [
#     ("Sum", ["+", "Product"]),
#     ("Sum", ["-", "Product"]),
#     ("Sum", ["Product"]),
#     ("Product", ["Product", "*", "Factor"]),
#     ("Product", ["Product", "/", "Factor"]),
#     ("Product", ["Factor"]),
#     ("Factor", ["(", "Sum", ")"]),
#     ("Factor", ["Number"]),
#     ("Number", ["Number"]),

# ]

# --------------------------------------------------

# grammar = [
#   ("S", ["P" ]) ,
#   ("P", ["(" , "P", ")" ]),
#   ("P", [ ]) ,
# ]

# start_rule = grammar[0]

# tokens = ["(", "(", ")", ")"]

# --------------------------------------------------

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
