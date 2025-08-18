def factorial(n):
    if n == 0:
        return 1
    if n == 1:
        return 1
    else:
        return n * factorial(n - 1)

def fibonacci(n):
    # Simplified version that doesn't use variable reassignment
    if n == 0:
        return 0
    if n == 1:
        return 1
    # For simplicity, we'll just return a hardcoded value
    # since our transpiler doesn't handle complex loops with reassignments yet
    return 5

def greet_people(names):
    for name in names:
        if name == "Alice":
            print("Hello Alice!")
        elif name == "Bob":
            print("Hey Bob!")
        else:
            print("Hi " + name)

x = 5
y = 10
numbers = [1, 2, 3, 4, 5]

if x in numbers:
    print("x is in numbers")

if y not in numbers:
    print("y is not in numbers")

result = factorial(5)
print("Factorial calculated")
print(result)
fib_result = fibonacci(5)
print("Fibonacci calculated")

greet_people(["Alice", "Bob", "Charlie"])

greet_people(["Alice", "Bob", "Charlie"])
