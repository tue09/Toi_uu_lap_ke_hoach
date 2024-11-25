from ortools.linear_solver import pywraplp
import sys

# # Tạo một solver
# solver = pywraplp.Solver.CreateSolver('GLOP') # Linear Programming
# solver = pywraplp.Solver.CreateSolver('SCIP') # Mixed-Integer Linear Programming

# # Khai báo các biến x và y với giới hạn dưới là 0
# x = solver.NumVar(0, solver.infinity(), 'x')
# y = solver.NumVar(0, solver.infinity(), 'y')

# # Đặt hàm mục tiêu: max(3x + 4y)
# solver.Maximize(3 * x + 4 * y)

# # Thêm các ràng buộc
# solver.Add(x + 2 * y <= 14)  # x + 2y <= 14
# solver.Add(3 * x - y >= 0)   # 3x - y >= 0
# solver.Add(x - y <= 2)       # x - y <= 2

# # Giải bài toán
# status = solver.Solve()

# # Kiểm tra và hiển thị kết quả
# if status == pywraplp.Solver.OPTIMAL:
#     print(f"Giá trị tối ưu: {solver.Objective().Value()}")
#     print(f"Giá trị của x: {x.solution_value()}")
#     print(f"Giá trị của y: {y.solution_value()}")
# elif status == pywraplp.Solver.FEASIBLE:
#     print("Không tìm thấy nghiệm tối ưu, nhưng có một nghiệm khả thi tốt nhất:")
#     print(f"Giá trị tốt nhất của hàm mục tiêu: {solver.Objective().Value()}")
#     print(f"Giá trị của x: {x.solution_value()}")
#     print(f"Giá trị của y: {y.solution_value()}")
# else:
#     print("Không tìm thấy nghiệm khả thi.")

solver = pywraplp.Solver.CreateSolver('GLOP') # Linear Programming
# solver = pywraplp.Solver.CreateSolver('SCIP') # Mixed-Integer Linear Programming

def solve_prob(n, m, DI, DUI, C, A, low, up):
    X = {}
    for i in range(n):
        X[i] = solver.NumVar(DI[i], DUI[i], '')
    for i in range(m):
        constraint_expr = solver.Sum(A[i][j] * X[j] for j in range(n))
        solver.Add(constraint_expr <= up[i])
        solver.Add(constraint_expr >= low[i])
        # solver.Add(solver.Sum([A[i][j] * X[j] for j in range(n)]) <= up[i])
        # solver.Add(solver.Sum([A[i][j] * X[j] for j in range(n)]) >= low[i])
        # solver.Add(X[i] <= DUI[i])
        # solver.Add(X[i] >= DI[i])
    solver.Maximize(solver.Sum([C[i] * X[i] for i in range(n)]))
    
    status = solver.Solve()

    # Kiểm tra và hiển thị kết quả
    if status == pywraplp.Solver.OPTIMAL:
        #print(f"Giá trị tối ưu: {solver.Objective().Value()}")
        print(n)
        for i in range(n):
            print(X[i].solution_value(), end = " ")
    # elif status == pywraplp.Solver.FEASIBLE:
    #     print("Không tìm thấy nghiệm tối ưu, nhưng có một nghiệm khả thi tốt nhất:")
    #     print(f"Giá trị Feasible tốt nhất của hàm mục tiêu: {solver.Objective().Value()}")
    #     print(f"Nghiem feasible tot nhat: ")
    #     for i in range(n):
    #         print(f"X[{i}] = {X[i].solution_value()}")
    else:
        print("NOT_OPTIMAL")

if __name__ == '__main__':
    n, m = map(int, sys.stdin.readline().split())
    DI, DUI = [], []
    for i in range(n):
        x, y = map(int, sys.stdin.readline().split())
        DI.append(x)
        DUI.append(y)
    C = [float(x) for x in sys.stdin.readline().split()]

    A = []
    for i in range(1, m+1):
        A.append([float(x) for x in sys.stdin.readline().split()])

    low = []
    up = []
    for i in range(1, m+1):
        x, y = map(int, sys.stdin.readline().split())
        low.append(x)
        up.append(y)

    solve_prob(n, m, DI, DUI, C, A, low, up)
