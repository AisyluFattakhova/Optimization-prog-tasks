import math


# Function to add matrices or vectors
def add_matrices(A, B):
    if isinstance(A[0], list):  # Check if A is a matrix
        rows = len(A)
        cols = len(A[0])
        # Create result matrix where each element is the sum of corresponding elements in A and B
        result = [[A[i][j] + B[i][j] for j in range(cols)] for i in range(rows)]
    else:  # If A is a vector
        result = [A[i] + B[i] for i in range(len(A))]
    if len(result) == 1:
        return result[0]
    return result


# Function to subtract matrices or vectors
def subtract_matrices(A, B):
    if isinstance(A[0], list):  # Check if A is a matrix
        rows = len(A)
        cols = len(A[0])
        # Create result matrix where each element is the difference of corresponding elements in A and B
        result = [[A[i][j] - B[i][j] for j in range(cols)] for i in range(rows)]
    else:  # If A is a vector
        result = [A[i] - B[i] for i in range(len(A))]
    if len(result) == 1:
        return result[0]
    return result


# Function to multiply matrices or vectors
def multiply_matrices(A, B):
    if isinstance(A[0], list) and isinstance(B[0], list):  # Matrix by matrix multiplication
        rows_A, cols_A = len(A), len(A[0])
        rows_B, cols_B = len(B), len(B[0])
        # Initialize result matrix with zeros
        result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
        for i in range(rows_A):
            for j in range(cols_B):
                for k in range(cols_A):
                    result[i][j] += A[i][k] * B[k][j]
    elif isinstance(B[0], list):  # Vector by matrix multiplication
        # Multiply vector A by each column of matrix B
        result = [sum(A[k] * B[k][j] for k in range(len(A))) for j in range(len(B[0]))]
    else:  # Matrix by vector multiplication
        # Multiply each row of matrix A by vector B
        result = [sum(A[j][k] * B[k] for k in range(len(B))) for j in range(len(A))]

    if len(result) == 1:
        return result[0]
    return result


# Function to calculate determinant of a matrix
def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:  # Base case for 2x2 matrix
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    det = 0
    # Calculate determinant using Laplace expansion
    for col in range(n):
        submatrix = [row[:col] + row[col + 1:] for row in matrix[1:]]
        sign = (-1) ** col
        det += sign * matrix[0][col] * determinant(submatrix)
    return det


# Function to transpose a matrix
def transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    # Create transposed matrix by switching rows and columns
    result = [[matrix[j][i] for j in range(rows)] for i in range(cols)]
    return result


# Function to calculate inverse of a matrix
def inverse_matrix(matrix):
    det = determinant(matrix)
    if det == 0:  # Check if matrix is invertible
        return False
    n = len(matrix)
    # Calculate adjugate matrix by finding minors and cofactors
    adjugate = [[(-1) ** (i + j) * determinant(
        [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]
    ) for j in range(n)] for i in range(n)]
    adjugate = transpose(adjugate)  # Transpose to get adjugate
    # Divide each element by determinant to get inverse
    inverse = [[adjugate[i][j] / det for j in range(n)] for i in range(n)]
    return inverse


# Input coefficients of objective function
c = list(map(int, input("Enter vector of coefficients of objective function:\n").split()))
N = len(c)

# Input coefficients of constraint functions until empty string is entered
A = []
a = list(map(int, input(
    "Enter a matrix of coefficients of constraint function. Enter empty string when you finish:\n").split()))

# Read rows of matrix A until an empty string is entered
while a != []:
    A.append(a)
    a = list(map(int, input().split()))
n = len(A)

# Input right-hand side numbers
B = list(map(int, input("Enter a vector of right-hand side numbers:\n").split()))

# Parameters for step adjustment
alpha_1 = 0.5
alpha_2 = 0.9

# Input accuracy for solution output
eps = float(input("Enter the accuracy for the answer:\n"))

# Create initial vector X0 with initial variables set to 1
X_0 = [1] * len(c)

# Add extra variables to objective vector c
for i in range(n):
    c.append(0)

# Fill initial vector X0 with values of extra variables
for i in range(n):
    X_0.append(B[i] - sum(A[i]))

# Append extra variables to matrix A to convert constraints
for i in range(n):
    for j in range(n):
        if i == j:
            A[i].append(1)
        else:
            A[i].append(0)

# Create identity matrix I with size of X0
I = [[1 if i == j else 0 for j in range(n)] for i in range(len(X_0))]

curr_step = 1  # Initialize iteration counter
flag = 0  # Flag for solution status
copyX_0 = X_0
copyA = A
copyc = c

while True:
    # Create diagonal matrix with elements of X0
    diag = [[X_0[i] if i == j else 0 for j in range(len(X_0))] for i in range(len(X_0))]

    # Calculate P matrix using intermediate steps
    A_ = multiply_matrices(A, diag)
    P = subtract_matrices(I, multiply_matrices(
        multiply_matrices(transpose(A_), inverse_matrix(multiply_matrices(A_, transpose(A_)))), A_))
    Cp = multiply_matrices(multiply_matrices(P, diag), c)
    v = min(Cp)

    if v >= 0:
        flag = 2
        break  # Stop if v is non-negative

    # Update step size and vector y
    v = abs(v)
    y = [1.0 + (alpha_1 / v) * Cp[j] for j in range(len(Cp))]
    y_ = multiply_matrices(diag, y)



    # Check convergence
    if math.sqrt(sum((y_[j] - X_0[j]) ** 2 for j in range(len(y_)))) < eps:
        flag = 0
        break
    if any(6.864552722525671e+34 < X_0[j] for j in range(len(X_0))):
        flag = 1
        break

    # Increment step and update X0
    curr_step += 1
    X_0 = y_

# Output results based on solution flag
if flag == 0:
    print("For a = 0.5 algorithm ends on iteration ", curr_step, ".")
    print("Optimal solution found:")
    z = sum(c[i] * X_0[i] for i in range(N))
    print("z = ", z)
    for k in range(1, N + 1):
        print(f"x{k} = {X_0[k - 1]}")
elif flag == 1:
    print("For a = 0.5: The problem does not have a solution!")
elif flag == 2:
    print("For a = 0.5: The method is not applicable!")


#Now we copy initial values and try algorithm with alpha_2 = 0.9
X_0 = copyX_0
A = copyA
c = copyc
curr_step = 1
flag = 0
while True:
    # Create diagonal matrix with elements of X0
    diag = [[X_0[i] if i == j else 0 for j in range(len(X_0))] for i in range(len(X_0))]

    # Calculate P matrix using intermediate steps
    A_ = multiply_matrices(A, diag)
    P = subtract_matrices(I, multiply_matrices(
        multiply_matrices(transpose(A_), inverse_matrix(multiply_matrices(A_, transpose(A_)))), A_))
    Cp = multiply_matrices(multiply_matrices(P, diag), c)
    v = min(Cp)

    if v >= 0:
        flag = 2
        break  # Stop if v is non-negative

    # Update step size and vector y
    v = abs(v)
    y = [1.0 + (alpha_2 / v) * Cp[j] for j in range(len(Cp))]
    y_ = multiply_matrices(diag, y)


    # Check convergence
    if math.sqrt(sum((y_[j] - X_0[j]) ** 2 for j in range(len(y_)))) < eps:
        flag = 0
        break
    if any(6.864552722525671e+34 < X_0[j] for j in range(len(X_0))):
        flag = 1
        break

    # Increment step and update X0
    curr_step += 1
    X_0 = y_

# Output results based on solution flag
if flag == 0:
    print("For a = 0.9 algorithm ends on iteration ", curr_step, ".")
    print("Optimal solution found:")
    z = sum(c[i] * X_0[i] for i in range(N))
    print("z = ", z)
    for k in range(1, N + 1):
        print(f"x{k} = {X_0[k - 1]}")
elif flag == 1:
    print("For a = 0.9: The problem does not have a solution!")
elif flag == 2:
    print("For a = 0.9: The method is not applicable!")
