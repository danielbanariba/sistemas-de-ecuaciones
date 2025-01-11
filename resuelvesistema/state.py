import reflex as rx
import numpy as np
from fractions import Fraction
from typing import List
import plotly.graph_objects as go

class State(rx.State):
    m: int = ""
    n: int = ""
    matrix_values: List[List[str]] = [["0" for _ in range(2)] for _ in range(2)]
    constants_values: List[str] = ["0" for _ in range(2)]
    result: str = ""
    solution: List[str] = []
    is_random: bool = False
    use_fractions: bool = True
    graph_data: go.Figure = go.Figure()
    show_graph: bool = False
    is_3d: bool = False

    def update_matrix(self):
        self.matrix_values = [["0" for _ in range(self.n)] for _ in range(self.m)]
        self.constants_values = ["0" for _ in range(self.m)]
        self.show_graph = False

    def set_matrix_value(self, i: int, j: int, value: str):
        self.matrix_values[i][j] = value
        self.show_graph = False

    def set_constant_value(self, i: int, value: str):
        self.constants_values[i] = value
        self.show_graph = False

    def parse_fraction(self, value: str) -> float:
        try:
            return float(Fraction(value))
        except ValueError:
            return 0.0

    def toggle_result_format(self):
        self.use_fractions = not self.use_fractions
        if self.result:
            self.solve_system()

    def format_result(self, solution):
        if self.use_fractions:
            return [f"x{i+1} = {Fraction(sol).limit_denominator()}" for i, sol in enumerate(solution)]
        else:
            return [f"x{i+1} = {sol:.4f}" for i, sol in enumerate(solution)]

    def solve_system(self):
        try:
            matrix = np.array([[self.parse_fraction(val) for val in row] for row in self.matrix_values])
            constants = np.array([self.parse_fraction(val) for val in self.constants_values])
            A = matrix
            b = constants

            rank_A = np.linalg.matrix_rank(A)
            rank_Ab = np.linalg.matrix_rank(np.column_stack((A, b)))

            if rank_A < rank_Ab:
                self.result = "El sistema no tiene solución."
                self.solution = []
            elif rank_A < A.shape[1]:
                self.result = "El sistema tiene infinitas soluciones."
                self.solution = []
            else:
                try:
                    solution = np.linalg.solve(A, b)
                    self.solution = self.format_result(solution)
                    self.result = "Solución encontrada"
                except np.linalg.LinAlgError:
                    self.result = "El sistema no tiene una solución única (matriz singular)."
                    self.solution = []
        except ValueError:
            self.result = "Error: Por favor, ingrese números o fracciones válidas en todas las celdas."
            self.solution = []
        
        self.update_graph()
        self.show_graph = self.m in [2, 3] and self.n in [2, 3]
        self.is_3d = (self.m == 3 and self.n == 3) or (self.m == 2 and self.n == 3)

    def solve_random(self):
        self.is_random = True
        coefficients = np.random.randint(-10, 11, size=(self.m, self.n)).astype(float)
        constants = np.random.randint(-10, 11, size=(self.m,)).astype(float)
        
        self.matrix_values = [[str(Fraction(val).limit_denominator()) for val in row] for row in coefficients.tolist()]
        self.constants_values = [str(Fraction(val).limit_denominator()) for val in constants.tolist()]
        
        self.solve_system()

    def clean_all(self):
        self.m = 2
        self.n = 2
        self.matrix_values = [["0" for _ in range(2)] for _ in range(2)]
        self.constants_values = ["0" for _ in range(2)]
        self.result = ""
        self.solution = []
        self.is_random = False
        self.show_graph = False
        self.is_3d = False
        self.update_graph()

    def update_graph(self):
        if self.m == 2 and self.n == 2:
            self.update_2d_graph()
        elif self.m == 3 and self.n == 3:
            self.update_3d_graph()
        elif (self.m == 2 and self.n == 3) or (self.m == 3 and self.n == 2):
            self.update_2x3_or_3x2_graph()
        else:
            self.graph_data = go.Figure()

    def update_2d_graph(self):
        coefficients = [[self.parse_fraction(val) for val in row] for row in self.matrix_values[:2]]
        constants = [self.parse_fraction(val) for val in self.constants_values[:2]]
        
        x = np.linspace(-10, 10, 100)
        y1 = [(constants[0] - coefficients[0][0] * xi) / coefficients[0][1] for xi in x]
        y2 = [(constants[1] - coefficients[1][0] * xi) / coefficients[1][1] for xi in x]

        det = coefficients[0][0] * coefficients[1][1] - coefficients[1][0] * coefficients[0][1]
        if det != 0:
            x_intersect = (constants[0] * coefficients[1][1] - constants[1] * coefficients[0][1]) / det
            y_intersect = (coefficients[0][0] * constants[1] - coefficients[1][0] * constants[0]) / det
        else:
            x_intersect = y_intersect = None

        self.graph_data = go.Figure()
        self.graph_data.add_trace(go.Scatter(x=x, y=y1, mode='lines', name=f"{coefficients[0][0]}x + {coefficients[0][1]}y = {constants[0]}", line=dict(color='blue')))
        self.graph_data.add_trace(go.Scatter(x=x, y=y2, mode='lines', name=f"{coefficients[1][0]}x + {coefficients[1][1]}y = {constants[1]}", line=dict(color='red')))
        if x_intersect is not None and y_intersect is not None:
            self.graph_data.add_trace(go.Scatter(x=[x_intersect], y=[y_intersect], mode='markers', marker=dict(size=10, color='green'), name='Intersección'))

        self.graph_data.update_layout(
            title="Sistema de Ecuaciones 2x2",
            xaxis_title="x",
            yaxis_title="y",
            width=600,
            height=400
        )

    def update_3d_graph(self):
        coefficients = [[self.parse_fraction(val) for val in row] for row in self.matrix_values[:3]]
        constants = [self.parse_fraction(val) for val in self.constants_values[:3]]

        x = y = np.linspace(-10, 10, 50)
        X, Y = np.meshgrid(x, y)

        Z1 = (constants[0] - coefficients[0][0] * X - coefficients[0][1] * Y) / coefficients[0][2]
        Z2 = (constants[1] - coefficients[1][0] * X - coefficients[1][1] * Y) / coefficients[1][2]
        Z3 = (constants[2] - coefficients[2][0] * X - coefficients[2][1] * Y) / coefficients[2][2]

        self.graph_data = go.Figure()
        self.graph_data.add_trace(go.Surface(x=X, y=Y, z=Z1, name=f"{coefficients[0][0]}x + {coefficients[0][1]}y + {coefficients[0][2]}z = {constants[0]}", colorscale='Blues', opacity=0.8))
        self.graph_data.add_trace(go.Surface(x=X, y=Y, z=Z2, name=f"{coefficients[1][0]}x + {coefficients[1][1]}y + {coefficients[1][2]}z = {constants[1]}", colorscale='Reds', opacity=0.8))
        self.graph_data.add_trace(go.Surface(x=X, y=Y, z=Z3, name=f"{coefficients[2][0]}x + {coefficients[2][1]}y + {coefficients[2][2]}z = {constants[2]}", colorscale='Greens', opacity=0.8))

        if self.solution:
            x, y, z = [self.parse_fraction(sol.split(" = ")[1]) for sol in self.solution]
            self.graph_data.add_trace(go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', marker=dict(size=5, color='yellow'), name='Solución'))

        self.graph_data.update_layout(
            title="Sistema de Ecuaciones 3x3",
            scene=dict(
                xaxis_title="x",
                yaxis_title="y",
                zaxis_title="z",
                aspectmode='cube'
            ),
            width=700,
            height=700
        )

    def update_2x3_or_3x2_graph(self):
        coefficients = [[self.parse_fraction(val) for val in row] for row in self.matrix_values[:3]]
        constants = [self.parse_fraction(val) for val in self.constants_values[:3]]

        if self.m == 2 and self.n == 3:  # 2x3 system
            self.plot_2x3_graph(coefficients[:2], constants[:2])
        elif self.m == 3 and self.n == 2:  # 3x2 system
            self.plot_3x2_graph(coefficients[:3], constants[:3])

    def plot_2x3_graph(self, coefficients, constants):
        x = y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)

        Z1 = (constants[0] - coefficients[0][0]*X - coefficients[0][1]*Y) / coefficients[0][2]
        Z2 = (constants[1] - coefficients[1][0]*X - coefficients[1][1]*Y) / coefficients[1][2]

        self.graph_data = go.Figure()
        self.graph_data.add_trace(go.Surface(x=X, y=Y, z=Z1, name=f"{coefficients[0][0]}x + {coefficients[0][1]}y + {coefficients[0][2]}z = {constants[0]}", colorscale='Blues', opacity=0.8))
        self.graph_data.add_trace(go.Surface(x=X, y=Y, z=Z2, name=f"{coefficients[1][0]}x + {coefficients[1][1]}y + {coefficients[1][2]}z = {constants[1]}", colorscale='Reds', opacity=0.8))

        self.graph_data.update_layout(
            title="Sistema de Ecuaciones 2x3",
            scene=dict(
                xaxis_title="x",
                yaxis_title="y",
                zaxis_title="z",
                aspectmode='cube'
            ),
            width=700,
            height=700
        )

    def plot_3x2_graph(self, coefficients, constants):
        x = np.linspace(-10, 10, 100)
        y1 = [(constants[0] - coefficients[0][0] * xi) / coefficients[0][1] for xi in x]
        y2 = [(constants[1] - coefficients[1][0] * xi) / coefficients[1][1] for xi in x]
        y3 = [(constants[2] - coefficients[2][0] * xi) / coefficients[2][1] for xi in x]

        self.graph_data = go.Figure()
        self.graph_data.add_trace(go.Scatter(x=x, y=y1, mode='lines', name=f"{coefficients[0][0]}x + {coefficients[0][1]}y = {constants[0]}", line=dict(color='blue')))
        self.graph_data.add_trace(go.Scatter(x=x, y=y2, mode='lines', name=f"{coefficients[1][0]}x + {coefficients[1][1]}y = {constants[1]}", line=dict(color='red')))
        self.graph_data.add_trace(go.Scatter(x=x, y=y3, mode='lines', name=f"{coefficients[2][0]}x + {coefficients[2][1]}y = {constants[2]}", line=dict(color='green')))

        self.graph_data.update_layout(
            title="Sistema de Ecuaciones 3x2",
            xaxis_title="x",
            yaxis_title="y",
            width=600,
            height=400
        )