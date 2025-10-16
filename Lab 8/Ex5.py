def fibonacci(list):
    Fibo = [0, 1]
    for val in list[1:]:
        Fibo.append(Fibo[-1] + val)
    return Fibo

my_list = [1, 2, 3, 4, 5]
print(fibonacci(my_list)) 