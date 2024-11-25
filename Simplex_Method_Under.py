from ortools.linear_solver import pywraplp
import sys

solver = pywraplp.Solver.CreateSolver('GLOP') # Linear Programming

def solve_prob(n, m, C, A, b):
    X = {}
    for i in range(n):
        X[i] = solver.NumVar(0, solver.infinity(), '')
    for i in range(m):
        solver.Add(solver.Sum([A[i][j] * X[j] for j in range(n)]) <= b[i])
    solver.Maximize(solver.Sum([C[i] * X[i] for i in range(n)]))
    
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(n)
        for i in range(n):
            print(round(X[i].solution_value(), 5), end = " ")
    else:
        print("UNBOUNDED")

if __name__ == '__main__':
    n, m = map(int, sys.stdin.readline().split())

    C = [float(x) for x in sys.stdin.readline().split()]

    A = []
    for i in range(1, m+1):
        A.append([float(x) for x in sys.stdin.readline().split()])

    b = [float(x) for x in sys.stdin.readline().split()]

    solve_prob(n, m, C, A, b)
