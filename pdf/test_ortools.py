from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP') 

x = solver.NumVar(0, solver.infinity(), 'x')
y = solver.NumVar(0, solver.infinity(), 'y')

solver.Maximize(3 * x + 4 * y)

solver.Add(x + 2 * y <= 14)
solver.Add(3 * x - y >= 0)
solver.Add(x - y <= 2)

status.solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(f"Gia tri toi uu: {solver.Objective().value()}")
    print(f"Gia tri cua x: {x.solution_value()}")
    print(f"Gia tri cua y: {y.solution_value()}")
else:
    print(f"Khong tim  thay nghiem toi uu")
