# Calculating the first 50 Fibonacci numbers together
def fibonacci_sum(n):
    # The first two Fibonacci numbers
    fib = [0, 1]

    # Adding the next n-2 Fibonacci numbers to the list
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])

    # Return the sum of the first n Fibonacci numbers
    return sum(fib)


# Print the sum of the first 50 Fibonacci numbers
def fib_print():
    print(fibonacci_sum(50))
