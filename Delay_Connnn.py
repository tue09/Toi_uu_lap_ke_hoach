import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
from ortools.linear_solver import pywraplp
import sys
from ortools.sat.python import cp_model


# solver = pywraplp.Solver.CreateSolver('GLOP') # Linear Programming
#solver = pywraplp.Solver.CreateSolver('SCIP') # Mixed-Integer Linear Programming
solver = cp_model.CpSolver()
# solver.parameters.max_time_in_seconds = 5.0
solver.parameters.num_search_workers = 1
model = cp_model.CpModel()
M = 10000
# n node, m num_edge, s source, L limit time
def solve_prob(n, m, s, L, graph, edge):
    X = {}
    Y = {}
    for i in range(n-1):
        X[i] = model.NewIntVar(1, n, '')
        Y[i] = model.NewIntVar(1, n, '')
        model.AddAllowedAssignments([X[i], Y[i]], edge)
    model.Add(X[0] >= s)
    model.Add(X[0] <= s)
    pair_vars = []
    for i in range(n-1):
        pair_var = model.NewIntVar(0, len(edge) - 1, '')
        model.AddElement(pair_var, [edge.index((x, y)) for (x, y) in edge], X[i])
        model.AddElement(pair_var, [edge.index((x, y)) for (x, y) in edge], Y[i])
        pair_vars.append(pair_var)

    model.AddAllDifferent(pair_vars)

    for i in range(1, n-1):
        # const1: X[i] == s
        # const2: X[i] in Y[:i-1]
        # model.Add(const1 or const2)
        const1 = model.NewBoolVar('')
        model.Add(X[i] == s).OnlyEnforceIf(const1)
        const2 = model.NewBoolVar('')
        #model.AddBoolOr([X[i] == Y[j] for j in range(i)]).OnlyEnforceIf(const2)
        bool_tues = []
        for j in range(i):
            bool_tue = model.NewBoolVar('')
            model.Add(X[i] == Y[j]).OnlyEnforceIf(bool_tue)
            model.Add(X[i] != Y[j]).OnlyEnforceIf(bool_tue.Not())
            bool_tues.append(bool_tue)
        model.AddBoolOr(bool_tues).OnlyEnforceIf(const2)
        model.AddBoolOr([const1, const2])


    model.minimize()

    status = solver.Solve(model)

    if status == pywraplp.Solver.OPTIMAL:
        print(f"{int(solver.Objective().Value())}")
    else:
        print("NO_SOLUTION")
    # else:
    #     print("NOT_FEASIBLE")

if __name__ == '__main__':
    n, m, s, L = map(int, sys.stdin.readline().split())

    graph_ = []
    edge = []
    for i in range(m):
        u, v, t, c = map(int, sys.stdin.readline().split())
        graph_.append((u, v, t, c))
        edge.append((u, v))

    solve_prob(n, m, s, L, graph_, edge)