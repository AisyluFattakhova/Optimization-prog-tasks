from typing import List
import copy

INF = 10 ** 10


# function counts the total cost of the transportation
def count_res(C: List[List[float]], Supplied: List[List[float]]):
    res = 0
    n = len(C)
    m = len(C[0])
    for i in range(n):
        for j in range(m):
            res += C[i][j] * Supplied[i][j]
    return res


# function applies north-west rule to get one of the solutions
def north_west(S: List[float], C: List[List[float]], D: List[float]):
    n = len(S)
    m = len(D)
    supplied = [[0 for _ in range(m)] for _ in range(n)]
    # processing the leftmost and upmost cell
    x, y = (0, 0)
    while x != n and y != m:
        # get the maximum possible supply which is demanded
        supplied[x][y] = min(S[x], D[y])
        S[x] -= supplied[x][y]
        D[y] -= supplied[x][y]
        # if the source is ran out, move to the next one
        if S[x] == 0 and x < n:
            x += 1
        # if the demand is met, move to the next one
        if D[y] == 0 and y < m:
            y += 1
    return supplied


# function to find row difference and column difference
def find_difference(A):
    row_diff = []
    col_diff = []
    for i in range(len(A)):
        arr = A[i][:]
        arr.sort()
        row_diff.append(arr[1] - arr[0])
    for col in range(len(A[0])):
        arr = [A[i][col] for i in range(len(A))]
        arr.sort()
        col_diff.append(arr[1] - arr[0])
    return row_diff, col_diff


# function for Vogel's approximation method
def vogel(S, D, A):
    # Initialize a matrix to store the quantities to be transported
    bf_sol = [[0 for _ in range(len(A[0]))] for _ in range(len(A))]

    # Continue until all supply or demand is fulfilled
    while max(S) != 0 and max(D) != 0:
        # Calculate the row and column differences to find the largest opportunity cost
        row, col = find_difference(A)
        max_el_row_dif = max(row)  # Maximum row difference
        max_el_col_dif = max(col)  # Maximum column difference

        # if the row difference max element is greater than or equal to column difference max element
        if max_el_row_dif > max_el_col_dif:
            # Select the row with the highest difference penalty
            for index, value in enumerate(row):
                if value == max_el_row_dif:
                    # Find the minimum cost in the selected row
                    min_elem_in_row = min(A[index])
                    for index2, value2 in enumerate(A[index]):
                        if value2 == min_elem_in_row:
                            # Calculate the quantity to transport based on the minimum of supply or demand
                            min_of_supply_or_demand = min(S[index], D[index2])
                            S[index] -= min_of_supply_or_demand  # Reduce supply
                            D[index2] -= min_of_supply_or_demand  # Reduce demand
                            bf_sol[index][index2] = min_of_supply_or_demand  # Store the quantity in solution matrix
                            # if demand is smaller, then the entire col is assigned very large value
                            # so that the col is eliminated for the next iteration
                            if D[index2] == 0:
                                for k in range(len(A)):
                                    A[k][index2] = INF  # Mark column as fulfilled
                            # if supply is smaller, then the entire row is assigned very large value
                            # so that the row is eliminated for the next iteration
                            else:
                                for i in range(len(A[0])):
                                    A[index][i] = INF  # Mark row as fulfilled
                            break
                    break
        else:
            # Select the column with the highest difference
            for index, value in enumerate(col):
                if value == max_el_col_dif:
                    # Find the minimum cost in the selected column
                    min_elem_in_col = INF
                    for j in range(len(A)):
                        min_elem_in_col = min(min_elem_in_col, A[j][index])
                    for index2 in range(len(A)):
                        value2 = A[index2][index]
                        if value2 == min_elem_in_col:
                            # Calculate the quantity to transport based on the minimum of supply or demand
                            min_of_supply_or_demand = min(S[index2], D[index])
                            S[index2] -= min_of_supply_or_demand  # Reduce supply
                            D[index] -= min_of_supply_or_demand  # Reduce demand
                            bf_sol[index2][index] = min_of_supply_or_demand  # Store the quantity in solution matrix

                            # if demand is smaller, then the entire col is assigned very large value
                            # so that the col is eliminated for the next iteration
                            if D[index] == 0:
                                for i in range(len(A)):
                                    A[i][index] = INF  # Mark column as fulfilled
                            # if supply is smaller, then the entire row is assigned very large value
                            # so that the row is eliminated for the next iteration
                            else:
                                A[index2] = [INF for _ in range(len(A[0]))]  # Mark row as fulfilled
                            break
                    break

    return bf_sol  # Return the final solution matrix containing quantities to transport


# function checks if all the values (costs, supplies and demand) are non-negative
def check_if_applicable(S, C, D):
    if any(x < 0 for x in S) or any(x < 0 for x in D) or any(x < 0 for x in C[i] for i in range(len(C))):
        print("The method is not applicable!")
        exit(0)


# function checks if the problem is balanced
def check_balance(S, D):
    if sum(S) != sum(D):
        print("The problem is not balanced!")
        exit(0)


# function prints the table with the initial costs, supplies and demand
def print_initial(S, C, D):
    for i in range(len(D)):
        print(f"\tD{i + 1}", end="")
    print("\tSupply")
    for i in range(len(S)):
        print(f"S{i + 1}\t", end="")
        for j in range(len(D)):
            print(f"{C[i][j]}\t", end="")
        print(S[i])
    print("Demand\t", end="")
    for x in D:
        print(f"{x}\t", end="")
    print()


def russel_approximation(S, C, D):
    # # Initialize the readiness vectors of rows and columns
    row_ready = [True] * len(S)
    column_ready = [True] * len(D)
    supplied = [[0] * len(D) for _ in range(len(S))]  # Supply matrix

    while True:
        u = [-1] * len(S)
        v = [-1] * len(D)

        # Find the maximum cost values ​​for rows and columns
        for y in range(len(S)):
            for x in range(len(D)):
                if not (row_ready[y] and column_ready[x]):
                    continue
                u[y] = max(u[y], C[y][x])
                v[x] = max(v[x], C[y][x])

        deltas = [[C[y][x] - u[y] - v[x] for x in range(len(D))] for y in range(len(S))]
        max_neg = 0
        coords = (-1, -1)

        # Find the maximum negative delta value
        for y in range(len(S)):
            for x in range(len(D)):
                if deltas[y][x] < 0 and deltas[y][x] < max_neg and row_ready[y] and column_ready[x]:
                    max_neg = deltas[y][x]
                    coords = (y, x)

        # If there are no negative delta values, complete the algorithm
        if max_neg == 0:
            break

        y, x = coords
        temp = min(S[y], D[x])
        S[y] -= temp
        D[x] -= temp
        supplied[y][x] = temp  # Filling out the supply matrix

        # Update readiness of rows and columns
        if S[y] == 0:
            row_ready[y] = False
        if D[x] == 0:
            column_ready[x] = False

    return supplied


# input the data
n, m = map(int, input("Enter dimentions (n m):\n").split())
try:
    C = [[0 for _ in range(m)] for _ in range(n)]
    S = list(map(float, input(f"Enter source vector ({n} float numbers):\n").split()))
    if len(S) != n:
        raise Exception("Incorrect dimensions")
    print(f"Enter cost matrix ({n} x {m} float numbers):")
    for i in range(n):
        line = list(map(float, input().split()))
        if len(line) != m:
            raise Exception("Incorrect dimensions")
        C[i] = line
    D = list(map(float, input(f"Enter demand vector ({m} float numbers):\n").split()))
    if len(D) != m:
        raise Exception("Incorrect dimensions")
    # check if the problem is correct
    check_if_applicable(S, C, D)
    check_balance(S, D)

    print_initial(S, C, D)

    # apply different methods on the copies of matrices and lists
    nw_matrix = north_west(S.copy(), copy.deepcopy(C), D.copy())
    vogel_matrix = vogel(S.copy(), D.copy(), copy.deepcopy(C))
    russel_matrix = russel_approximation(S.copy(), copy.deepcopy(C), D.copy())

    # output the results
    print("North-West Corner Rule:")
    print(nw_matrix)
    print(f"Z = {count_res(C, nw_matrix)}")

    print("Vogel's Approximation:")
    print(vogel_matrix)
    print(f"Z = {count_res(C, vogel_matrix)}")

    print("Russel's Approximation:")
    print(russel_matrix)
    print(f"Z = {count_res(C, russel_matrix)}")
# if incorrect number of elements were given error Incorrect dimensions raised
except Exception as err:
    print(err)
