def factorial(n) :  # Build the factorial mechanism
    sum = 1

    for i in range(2, n + 1) :
        sum *= i
        
    return sum