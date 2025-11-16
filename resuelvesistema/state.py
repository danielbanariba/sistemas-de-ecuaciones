import reflex as rx
import numpy as np
from fractions import Fraction
from decimal import InvalidOperation
from typing import List
import plotly.graph_objects as go

class State(rx.State):
    m: str = ""
    n: str = ""
    matrix_values: List[List[str]] = [["0" for _ in range(2)] for _ in range(2)]
    constants_values: List[str] = ["0" for _ in range(2)]
    result: str = ""
    solution: List[str] = []
    solution_steps: List[str] = []
    equations_display: List[str] = []
    matrix_A_display: List[List[str]] = []
    vector_b_display: List[str] = []
    variables_list: List[str] = []
    rank_A: int = 0
    rank_Ab: int = 0
    num_variables: int = 0
    conclusion_text: str = ""
    is_random: bool = False
    use_fractions: bool = True
    graph_data: go.Figure = go.Figure()
    show_graph: bool = False
    is_3d: bool = False
    is_solving: bool = False
    validation_error: str = ""

    @rx.var
    def m_int(self) -> int:
        try:
            val = int(self.m) if self.m else 2
            return max(1, min(10, val))  # Limitar entre 1 y 10
        except ValueError:
            return 2

    @rx.var
    def n_int(self) -> int:
        try:
            val = int(self.n) if self.n else 2
            return max(1, min(10, val))  # Limitar entre 1 y 10
        except ValueError:
            return 2

    def set_m(self, value: str):
        self.m = value
        self._validate_dimensions()

    def set_n(self, value: str):
        self.n = value
        self._validate_dimensions()

    def _validate_dimensions(self):
        """Validar dimensiones en tiempo real"""
        try:
            m_val = int(self.m) if self.m else 2
            n_val = int(self.n) if self.n else 2
            if m_val < 1 or m_val > 10 or n_val < 1 or n_val > 10:
                self.validation_error = "Las dimensiones deben estar entre 1 y 10"
            else:
                self.validation_error = ""
        except ValueError:
            if self.m or self.n:
                self.validation_error = "Ingrese números válidos"
            else:
                self.validation_error = ""

    def update_matrix(self):
        self.matrix_values = [["0" for _ in range(self.n_int)] for _ in range(self.m_int)]
        self.constants_values = ["0" for _ in range(self.m_int)]
        self.show_graph = False

    def set_matrix_value(self, i: int, j: int, value: str):
        self.matrix_values[i][j] = value
        self.show_graph = False

    def set_constant_value(self, i: int, value: str):
        self.constants_values[i] = value
        self.show_graph = False

    def parse_fraction(self, value: str) -> float:
        try:
            return float(Fraction(value.strip()))
        except (ValueError, ZeroDivisionError, InvalidOperation, TypeError):
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
        self.is_solving = True
        self.solution_steps = []
        self.equations_display = []
        self.matrix_A_display = []
        self.vector_b_display = []
        self.conclusion_text = ""

        try:
            matrix = np.array([[self.parse_fraction(val) for val in row] for row in self.matrix_values])
            constants = np.array([self.parse_fraction(val) for val in self.constants_values])
            A = matrix
            b = constants

            # Generar visualización del sistema de ecuaciones
            self._generate_equations_display(A, b)

            # Generar visualización de matrices
            self._generate_matrix_display(A, b)

            self.rank_A = int(np.linalg.matrix_rank(A))
            self.rank_Ab = int(np.linalg.matrix_rank(np.column_stack((A, b))))
            self.num_variables = int(A.shape[1])

            if self.rank_A < self.rank_Ab:
                self.result = "Sistema Inconsistente"
                self.solution = []
                self.conclusion_text = "El sistema NO tiene solución porque Rango(A) < Rango(A|b). Las ecuaciones son contradictorias."
            elif self.rank_A < A.shape[1]:
                self.result = "Sistema Indeterminado"
                self.solution = []
                self.conclusion_text = "El sistema tiene INFINITAS soluciones porque Rango(A) < número de variables. Hay variables libres."
            else:
                try:
                    solution = np.linalg.solve(A, b)
                    self.solution = self.format_result(solution)
                    self.result = "Solución Única Encontrada"
                    self.conclusion_text = "El sistema tiene UNA solución única porque Rango(A) = Rango(A|b) = número de variables."
                except np.linalg.LinAlgError:
                    self.result = "Matriz Singular"
                    self.solution = []
                    self.conclusion_text = "La matriz es singular y no se puede resolver directamente."
        except ValueError as e:
            self.result = f"Error de entrada"
            self.solution = []
            self.conclusion_text = f"Por favor, ingrese números o fracciones válidas. ({str(e)})"
        except Exception as e:
            self.result = f"Error inesperado"
            self.solution = []
            self.conclusion_text = str(e)
        finally:
            self.is_solving = False

        self.update_graph()
        self.show_graph = self.m_int in [2, 3] and self.n_int in [2, 3]
        self.is_3d = (self.m_int == 3 and self.n_int == 3) or (self.m_int == 2 and self.n_int == 3)

    def _generate_equations_display(self, A, b):
        """Generar representación visual del sistema de ecuaciones"""
        var_names = [f"x{i+1}" for i in range(A.shape[1])]
        equations = []

        for i in range(A.shape[0]):
            terms = []
            for j in range(A.shape[1]):
                coef = Fraction(A[i, j]).limit_denominator()
                if coef == 0:
                    continue
                elif coef == 1:
                    term = f"+{var_names[j]}" if terms else var_names[j]
                elif coef == -1:
                    term = f"-{var_names[j]}"
                elif coef > 0:
                    term = f"+{coef}{var_names[j]}" if terms else f"{coef}{var_names[j]}"
                else:
                    term = f"{coef}{var_names[j]}"
                terms.append(term)

            if not terms:
                terms = ["0"]

            equation = " ".join(terms) + f" = {Fraction(b[i]).limit_denominator()}"
            equations.append(equation)

        self.equations_display = equations

    def _generate_matrix_display(self, A, b):
        """Generar representación visual de las matrices"""
        self.matrix_A_display = [
            [str(Fraction(val).limit_denominator()) for val in row]
            for row in A
        ]
        self.vector_b_display = [str(Fraction(val).limit_denominator()) for val in b]
        self.variables_list = [f"x{i+1}" for i in range(A.shape[1])]

    def solve_random(self):
        self.is_random = True
        coefficients = np.random.randint(-10, 11, size=(self.m_int, self.n_int)).astype(float)
        constants = np.random.randint(-10, 11, size=(self.m_int,)).astype(float)
        
        self.matrix_values = [[str(Fraction(val).limit_denominator()) for val in row] for row in coefficients.tolist()]
        self.constants_values = [str(Fraction(val).limit_denominator()) for val in constants.tolist()]
        
        self.solve_system()

    def clean_all(self):
        self.m = "2"
        self.n = "2"
        self.matrix_values = [["0" for _ in range(2)] for _ in range(2)]
        self.constants_values = ["0" for _ in range(2)]
        self.result = ""
        self.solution = []
        self.solution_steps = []
        self.equations_display = []
        self.matrix_A_display = []
        self.vector_b_display = []
        self.variables_list = []
        self.rank_A = 0
        self.rank_Ab = 0
        self.num_variables = 0
        self.conclusion_text = ""
        self.is_random = False
        self.show_graph = False
        self.is_3d = False
        self.validation_error = ""
        self.update_graph()

    def update_graph(self):
        if self.m_int == 2 and self.n_int == 2:
            self.update_2d_graph()
        elif self.m_int == 3 and self.n_int == 3:
            self.update_3d_graph()
        elif (self.m_int == 2 and self.n_int == 3) or (self.m_int == 3 and self.n_int == 2):
            self.update_2x3_or_3x2_graph()
        else:
            self.graph_data = go.Figure()

    def update_2d_graph(self):
        coefficients = [[self.parse_fraction(val) for val in row] for row in self.matrix_values[:2]]
        constants = [self.parse_fraction(val) for val in self.constants_values[:2]]

        # Verificar división por cero
        if coefficients[0][1] == 0 or coefficients[1][1] == 0:
            self.graph_data = go.Figure()
            self.graph_data.add_annotation(
                text="No se puede graficar: coeficiente de y es cero",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return

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

        # Verificar división por cero
        if any(coefficients[i][2] == 0 for i in range(3)):
            self.graph_data = go.Figure()
            self.graph_data.add_annotation(
                text="No se puede graficar: coeficiente de z es cero en alguna ecuación",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return

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

        if self.m_int == 2 and self.n_int == 3:  # 2x3 system
            self.plot_2x3_graph(coefficients[:2], constants[:2])
        elif self.m_int == 3 and self.n_int == 2:  # 3x2 system
            self.plot_3x2_graph(coefficients[:3], constants[:3])

    def plot_2x3_graph(self, coefficients, constants):
        # Verificar división por cero
        if coefficients[0][2] == 0 or coefficients[1][2] == 0:
            self.graph_data = go.Figure()
            self.graph_data.add_annotation(
                text="No se puede graficar: coeficiente de z es cero",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return

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
        # Verificar división por cero
        if any(coefficients[i][1] == 0 for i in range(3)):
            self.graph_data = go.Figure()
            self.graph_data.add_annotation(
                text="No se puede graficar: coeficiente de y es cero en alguna ecuación",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
            return

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