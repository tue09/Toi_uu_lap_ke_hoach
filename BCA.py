import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from ortools.linear_solver import pywraplp
import sys
from ortools.sat.python import cp_model


# solver = pywraplp.Solver.CreateSolver('GLOP') # Linear Programming
solver = pywraplp.Solver.CreateSolver('SCIP') # Mixed-Integer Linear Programming
#solver = cp_model.CpSolver()
# solver.parameters.max_time_in_seconds = 5.0
# solver.parameters.num_search_workers = 1

# m teachers, n courses
def solve_prob(n, m, k, teacher, conflict):
    X = {}
    for i in range(m):
        for j in range(n):
            X[i, j] = solver.IntVar(0, 1, '')
    for i in range(m):
        for j in range(1, n+1):
            if j not in teacher[i]:
                solver.Add(X[i, j-1] <= 0)
    for i in range(m):
        for (j, k) in conflict:
            solver.Add(X[i, j-1] + X[i, k-1] <= 1)
    for j in range(n):
        solver.Add(solver.Sum([X[i, j] for i in range(m)]) >= 1)
    z = solver.IntVar(0, 10000, '')
    for i in range(m):
        solver.Add(z >= solver.Sum(X[i, j] for j in range(n)))
    solver.Minimize(z)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f"{int(solver.Objective().Value())}")
    else:
        print("-1")
    # else:
    #     print("NOT_FEASIBLE")

if __name__ == '__main__':
    m, n = map(int, sys.stdin.readline().split())

    teacher = []
    for i in range(m):
        teacher.append([int(i) for i in sys.stdin.readline().split()][1:])
    k = int(sys.stdin.readline().strip())
    conflict = []
    for i in range(k):
        u, v = map(int, sys.stdin.readline().split())
        conflict.append((u, v))

    solve_prob(n, m, k, teacher, conflict)