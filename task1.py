def round_to_eps(a, eps):
    """
    Rounds a float value to a specified number of decimal places.

    Args:
        a (float): The input float value.
        eps (int): The number of decimal places to round to.

    Returns:
        str: The rounded value as a string with the specified number of decimal places.
    """
    # Round the float value
    rounded_value = round(a, eps)

    # Convert to string and ensure correct number of decimal places
    result_str = f"{rounded_value:.{eps}f}"

    return result_str


def function_to_check_the_correctness_of_the_table(vector):
    """
    Checks if there are negative values in the first row of the table.

    Args:
        vector (list): The table represented as a list of lists.

    Returns:
        bool: True if there are negative values, False otherwise.
    """
    for i in vector[0]:
        if i < 0:
            return True
    return False


# Input coefficients of objective function
c = list(map(int, input("Enter vector of coefficients of objective function:\n").split()))

# Input coefficients of constraint functions until empty string is entered
A = []
a = list(map(int, input(
    "Enter a matrix of coefficients of constraint function. Enter empty string when you finish:\n").split()))
while (a != []):
    A.append(a)
    a = list(map(int, input().split()))
n = len(A)

# Input right-hand side numbers
B = list(map(int, input("Enter a vector of right-hand side numbers:\n").split()))
b = [0]  # Include 0 at the beginning for the objective function

for i in range(len(B)):
    b.append(B[i])

# Input precision for output
eps = int(input("Enter the number of decimal places in the answer:\n"))

# Create leftmost column header
d = list(("z " + (n - 1) * "s " + "s").split())

# Initialize full table including constraints and objective function
full_table = []
for i in range(len(c)):
    c[i] *= -1  # Change signs when moving to objective function
full_table.append(c)
for i in range(n):
    full_table.append(A[i])

flag = 1
# Flag to indicate if a valid pivot was found

while function_to_check_the_correctness_of_the_table(full_table) and flag == 1:
    flag = 0
    pivot = 0
    pivot_index = 0
    for i in range(len(full_table[0])):  # Choose column based on first row
        if full_table[0][i] < pivot:
            pivot_index = i
            pivot = full_table[0][i]

    row_pivot = 1000000000000
    row_index = 0
    for i in range(1, len(full_table)):
        # Choose row
        if full_table[i][pivot_index] != 0 and b[i] / full_table[i][pivot_index] > 0 and b[i] / full_table[i][
            pivot_index] < row_pivot:
            row_pivot = b[i] / full_table[i][pivot_index]
            row_index = i
            flag = 1  # Set flag if a pivot is found

    d[row_index] = (pivot_index + 1)  # Update column header
    b[row_index] = row_pivot  # Divide free coefficients column by pivot
    pivot_value = full_table[row_index][pivot_index]  # Find pivot value
    for j in range(len(full_table[row_index])):
        full_table[row_index][j] /= pivot_value
    for i in range(n + 1):
        if i != row_index:
            ratio = full_table[i][pivot_index]  # Find ratio for elimination
            b[i] -= row_pivot * ratio  # Eliminate pivot column
            for j in range(len(full_table[i])):
                full_table[i][j] -= full_table[row_index][j] * ratio

if flag == 1:  # If valid pivots were found each time
    values = dict()
    for i in range(n + 1):
        if i == 0:
            print("z = ", round_to_eps(b[i], eps))  # Print objective function value
        else:
            if d[i] != "s":
                values[d[i]] = b[i]  # Add known variables to dictionary
    answer = dict(sorted(values.items(), key=lambda item: item[0]))  # Sort variables
    for k in range(1, len(c) + 1):
        if k in answer.keys():
            print("x", end="")
            print(k, end="")
            print(" = ", end="")
            print(round_to_eps(answer[k], eps))
        else:
            print("x", end="")
            print(k, end="")
            print(" = 0")
else:
    print("There is no feasible solution. Function is unbounded")
