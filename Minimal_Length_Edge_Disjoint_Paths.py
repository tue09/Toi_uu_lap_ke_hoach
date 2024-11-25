import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from ortools.linear_solver import pywraplp
import sys

# solver = pywraplp.Solver.CreateSolver('GLOP') # Linear Programming
solver = pywraplp.Solver.CreateSolver('SCIP') # Mixed-Integer Linear Programming

def solve_prob(n, m, edge, cost):
    X = {}
    for (i, j) in edge:
        X[i, j, 1] = solver.IntVar(0, 1, '')
        X[i, j, 2] = solver.IntVar(0, 1, '')
        solver.Add(X[i, j, 1] + X[i, j, 2] <= 1)
    
    for k in [1, 2]:
        for v in range(1, n+1):
            inflow = solver.Sum(X[i, v, k] for (i, j) in edge if j == v)
            outflow = solver.Sum(X[v, j, k] for (i, j) in edge if i == v)
            if v == 1:
                solver.Add(outflow - inflow == 1)
            elif v == n:
                solver.Add(inflow - outflow == 1)
            else:
                solver.Add(inflow - outflow == 0)

    X1 = solver.Sum([cost[i] * X[edge[i][0], edge[i][1], 1] for i in range(m)])
    X2 = solver.Sum([cost[i] * X[edge[i][0], edge[i][1], 2] for i in range(m)])
    solver.Minimize(solver.Sum([X1, X2]))
    
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f"{int(solver.Objective().Value())}")
    else:
        print("NOT_FEASIBLE")
    # else:
    #     print("NOT_FEASIBLE")

if __name__ == '__main__':
    n, m = map(int, sys.stdin.readline().split())

    edge = []
    cost = []

    for i in range(m):
        u, v, c = map(int, sys.stdin.readline().split())
        edge.append((u, v))
        cost.append(c)

    solve_prob(n, m, edge, cost)