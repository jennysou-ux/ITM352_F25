# Algorithm for multiplying two numbers

def multiply(a, b):
    product = 0
    for _ in range(b):
        product += a
    return product

first = int(input("Enter the first number: "))
second = int(input("Enter the second number: "))
prod = multiply(first, second)

print(f"The product of {first} and {second} is {prod}")

