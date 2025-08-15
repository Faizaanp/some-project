from lexer import tokenize
import os

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

def main():
    examples_dir = "examples"

    for filename in os.listdir(examples_dir):
        if filename.endswith(".py"):
            filepath = os.path.join(examples_dir, filename)
            print(f"Running {filename}:")
            with open(filepath, "r") as file:
                code = file.read()
                exec(code)

if __name__ == "__main__":
    main()
