from lexer import tokenize

code = """
def greet(name):
    print("Hello")
    print("World")
    if condition:
        print("Condition is true")
    else:
        print("Condition is false")
    # This is a comment
     
"""

tokens = tokenize(code)
for t in tokens:
    print(t)
