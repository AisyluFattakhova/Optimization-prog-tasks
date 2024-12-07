import numpy as np
 
def bisection_method():
    # Function to be analyzed
    def f(x):
        return x**3 - 6*x**2 + 11*x - 6  # Define the polynomial function
 
    # Input the interval bounds [a, b] and tolerance eps
    a, b = map(float, input("Enter the interval borders (a b): ").split())
    eps = float(input("Enter tolerance (eps): "))
 
    # Check if the provided interval is valid (root must lie between a and b)
    if f(a) * f(b) >= 0:
        print("Incorrect interval. Choose borders on different sides of the root.")
        exit(0)  # Exit if the function values at a and b do not change sign
 
    c = (a + b) / 2  # Calculate the initial midpoint
 
    # Iterate until the function value at c is within the specified tolerance
    while f(c) >= eps:
        if f(c) * f(a) < 0:  # If the root lies between a and c
            b = c  # Update the upper bound
        else:  # If the root lies between c and b
            a = c  # Update the lower bound
        c = (a + b) / 2  # Recalculate the midpoint
    print(f"The root is near {c:2.5f}")  # Print the approximated root
 
 
def golden_section():
    # Function to be minimized
    def f(x):
        return (x - 2)**2 + 3  # A simple quadratic function
 
    # Input the interval bounds [a, b] and tolerance eps
    a, b = map(float, input("Enter the interval borders (a b): ").split())
    eps = float(input("Enter tolerance (eps): "))
 
    # Define the golden ratio constant
    tau = (np.sqrt(5) - 1) / 2
 
    # Iterate until the interval size is less than the tolerance
    while b - a >= eps:
        # Calculate the two intermediate points within the interval
        x1 = b - tau * (b - a)
        y1 = f(x1)
        x2 = a + tau * (b - a)
        y2 = f(x2)
 
        # Compare the function values to decide which subinterval to keep
        if y1 < y2:  # Minimum lies in [a, x2]
            b = x2  # Update the upper bound
        else:  # Minimum lies in [x1, b]
            a = x1  # Update the lower bound
 
    c = (a + b) / 2  # The midpoint of the final interval is the approximate minimum
    print(f"x_min is near {c:2.5f}")  # Print the approximated minimum point
    print(f"f(x_min) is near {f(c):2.5f}")  # Print the function value at the minimum
 
 
def gradient_ascent_method():
    # Function to be maximized
    def f(x):
        return -x**2 + 4*x + 1  # A concave quadratic function
 
    # Derivative of the function (gradient)
    def f_prime(x):
        return -2*x + 4  # Gradient of f(x)
 
    # Input the initial guess, learning rate, and number of iterations
    x0 = float(input("Enter initial guess (x0): "))
    alpha = float(input("Enter learning rate (alpha): "))
    N = int(input("Enter number of iterations (N): "))
 
    X = x0  # Initialize the starting point
 
    # Iterate to update X using the gradient ascent formula
    for i in range(N):
        X = X + alpha * f_prime(X)  # Update the position in the direction of the gradient
 
    # Print the approximate maximum point and the function value at that point
    print(f"x_max is near {X:2.5f}")
    print(f"f(x_max) is near {f(X):2.5f}")
