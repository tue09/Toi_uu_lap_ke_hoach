import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from ortools.linear_solver import pywraplp
import sys

def solve_prob(n, C):
    solver = pywraplp.Solver.CreateSolver('CBC')  # Faster MILP solver

    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = solver.BoolVar(f'x_{i}_{j}')

    solver.Minimize(solver.Sum(C[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j))

    for i in range(n):
        solver.Add(solver.Sum(x[i, j] for j in range(n) if i != j) == 1)

    for j in range(n):
        solver.Add(solver.Sum(x[i, j] for i in range(n) if i != j) == 1)

    #remove subtour
    u = {i: solver.NumVar(0, n - 1, f'u_{i}') for i in range(1, n)}
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                solver.Add(u[i] - u[j] + n * x[i, j] <= n - 1)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(x[1, 0].solution_value())
        tour = []
        current_city = 0
        visited = set()
        while len(visited) < n:
            tour.append(current_city)
            visited.add(current_city)
            for j in range(n):
                if j != current_city and x[current_city, j].solution_value() == 1:
                    current_city = j
                    break
        print(n)
        for city in tour:
            print(city + 1, end=" ")
    else:
        print("NOT_OPTIMAL")

if __name__ == '__main__':
    n = int(sys.stdin.readline().strip())
    C = [list(map(float, sys.stdin.readline().split())) for _ in range(n)]
    solve_prob(n, C)

