import sys
from ortools.linear_solver import pywraplp

def solve_broadcast_tree():
    n, m, s, L = map(int, sys.stdin.readline().split())
    edges = []
    c = {}
    t = {}
    nodes = set()
    for _ in range(m):
        u, v, t_ij, c_ij = map(int, sys.stdin.readline().split())
        edges.append((u, v))
        c[(u, v)] = c_ij
        c[(v, u)] = c_ij
        t[(u, v)] = t_ij
        t[(v, u)] = t_ij
        nodes.update([u, v])

    nodes = list(nodes)
    arcs = []
    for (u, v) in edges:
        arcs.append((u, v))
        arcs.append((v, u))

    solver = pywraplp.Solver.CreateSolver('SCIP')

    x = {}
    f = {}
    t_arrival = {}

    for (i, j) in arcs:
        x[i, j] = solver.IntVar(0, 1, f'x_{i}_{j}')
        f[i, j] = solver.NumVar(0, n - 1, f'f_{i}_{j}')

    for i in nodes:
        t_arrival[i] = solver.NumVar(0, solver.infinity(), f't_{i}')

    M = 10000000

    # Constraints
    for (u, v) in edges:
        solver.Add(x[u, v] + x[v, u] <= 1)

    for i in nodes:
        if i == s:
            solver.Add(
                sum(f[s, k] for (s_, k) in arcs if s_ == s) -
                sum(f[k, s] for (k, s_) in arcs if s_ == s) == n - 1
            )
        else:
            solver.Add(
                sum(f[j, i] for (j, i_) in arcs if i_ == i) -
                sum(f[i, k] for (i_, k) in arcs if i_ == i) == 1
            )

    for (i, j) in arcs:
        solver.Add(f[i, j] <= (n - 1) * x[i, j])

    solver.Add(t_arrival[s] == 0)
    for (i, j) in arcs:
        solver.Add(
            t_arrival[j] >= t_arrival[i] + t[i, j] - M * (1 - x[i, j])
        )

    for i in nodes:
        solver.Add(t_arrival[i] <= L)

    objective = solver.Objective()
    for (i, j) in arcs:
        objective.SetCoefficient(x[i, j], c[i, j])
    objective.SetMinimization()

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        total_cost = sum(c[i, j] * x[i, j].solution_value() for (i, j) in arcs)
        print(int(total_cost))
    else:
        print('NO_SOLUTION')

if __name__ == '__main__':
    solve_broadcast_tree()
