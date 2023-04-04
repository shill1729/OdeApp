import numpy as np
import sympy as sp
from tabulate import tabulate


def complex_to_real(F, vars_list):
    # Create a list of new variables
    new_vars = []
    for var in vars_list:
        new_vars.extend([sp.re(var), sp.im(var)])

    # Create a list of new functions
    new_F = []
    for f in F:
        new_f = []
        for var in vars_list:
            new_f.extend([sp.re(f.subs(var, sp.re(var) + sp.im(var) * sp.I)),
                          sp.im(f.subs(var, sp.re(var) + sp.im(var) * sp.I))])
        new_F.append(new_f)

    return new_F, new_vars


class DynamicSystem:
    def __init__(self, F, x):
        self.F = F
        self.x = x
        self.fixed_points = self._solve_system()

    def _solve_system(self):
        # Convert the input lists to sympy expressions
        F = sp.Matrix(self.F)
        x = sp.Matrix(self.x)
        # Find the solutions to the system F(x) = 0
        sol = sp.solve(self.F, self.x)
        if type(sol) is dict:
            if len(sol) > 1:
                sol = sp.Matrix([sp.simplify(sol[w]) for w in x])
            else:
                sol = sp.Matrix([sol[x[0]]])
        else:
            sol = sp.Matrix(sol).T
        return sp.simplify(sol)

    def stability_analysis(self):
        # Find the fixed points of the system F(x) = 0
        fixed_points = self.fixed_points

        # Print the fixed points
        print("Fixed points:")
        print(fixed_points)

        # Define the Jacobian matrix
        J = sp.Matrix(self.F).jacobian(self.x)
        print("Jacobian matrix", J)
        table = []
        # Perform linear stability analysis at each fixed point
        for i in range(fixed_points.shape[1]):
            point = fixed_points[:, i]
            pt_display = point.tolist()
            pt_display = [w[0] for w in pt_display]
            J_fixed = J
            for j in range(len(point)):
                # Evaluate the Jacobian matrix at the fixed point
                J_fixed = J_fixed.subs(self.x[j], point[j])
            print("Jacobian at point:", J_fixed)

            # Alternative: just compute the trace and determinant
            # using the notation of Strogatz:
            tau = sp.simplify(sp.Trace(J_fixed))
            Delta = sp.simplify(J_fixed.det())
            print("Determinant of Jacobian at fixed point = " + str(pt_display))
            print(Delta)
            print("Trace of Jacobian at Fixed_point")
            print(tau)
            if sp.im(Delta) != 0:
                UserWarning(
                    "This system has some fixed points that are complex valued. Consider extending the system to higher dim.")
                break
            stability = ""
            if Delta < 0:
                stability = "saddle point"
            elif Delta > 0:
                if tau < 0:
                    stability = "stable"
                elif tau > 0:
                    stability = "unstable"
                elif tau == 0:
                    stability = "neutrally stable"
                if tau ** 2 - 4 * Delta > 0:
                    stability = stability + " nodes"
                elif tau ** 2 - 4 * Delta < 0:
                    stability = stability + " spiral"
                elif tau ** 2 - 4 * Delta == 0:
                    stability = stability + " star/degenerate nodes"
            elif Delta == 0:
                stability = "line of fixed points"

            table.append(
                ["Point: " + str(pt_display), tabulate([[stability]], headers=['Stability'], tablefmt='plain')])
        # print(tabulate(table, headers=['Fixed point', 'Stability analysis'], tablefmt='fancy_grid'))
        return tabulate(table, headers=['Fixed point', 'Stability analysis'], tablefmt='fancy_grid')

    def plot_phase_space(self, rect, i, j, ax):
        # Create a grid of points in the specified rectangle
        n = 50
        x_range = np.linspace(rect[0], rect[1], n)
        y_range = np.linspace(rect[2], rect[3], n)
        X, Y = np.meshgrid(x_range, y_range)

        # Evaluate the vector field at each point in the grid
        U = np.zeros_like(X)
        V = np.zeros_like(Y)
        for m in range(n):
            for k in range(n):
                point = [X[m, k], Y[m, k]]
                vec = [f.evalf(subs=dict(zip(self.x, point))) for f in self.F]
                U[m, k], V[m, k] = vec[i], vec[j]

        # Create a plot of the vector field
        # fig, ax = plt.subplots(figsize=(8, 8))
        ax.quiver(X[::3, ::3], Y[::3, ::3], U[::3, ::3], V[::3, ::3],
                  color='black', alpha=0.9, pivot="mid", units="inches")

        # Find the fixed points of the system
        fixed_points = self.fixed_points

        # Mark the fixed points on the plot
        for k in range(fixed_points.shape[1]):
            point = fixed_points[:, k]
            if sp.im(point[0]) != 0 or sp.im(point[1]) != 0:
                break
            if len(fixed_points[:, k]) > 1:
                c1 = isinstance(fixed_points[0, k], sp.Symbol)
                c2 = isinstance(fixed_points[1, k], sp.Symbol)
                if not c1 and not c2:
                    ax.plot(sp.re(fixed_points[i, k]), sp.re(fixed_points[j, k]), 'bo')
            else:
                c1 = isinstance(fixed_points[0, k], sp.Symbol)
                if not c1:
                    ax.plot(sp.re(fixed_points[i, k]), sp.re(fixed_points[j, k]), 'bo')

        # Label the axes
        ax.set_xlabel('x' + str(i + 1))
        ax.set_ylabel('x' + str(j + 1))

        # Show the plot
        # plt.show()