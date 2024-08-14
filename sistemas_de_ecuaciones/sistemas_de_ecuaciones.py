import reflex as rx
import numpy as np
from fractions import Fraction
from typing import List
import plotly.graph_objects as go

class State(rx.State):
    m: int = 2
    n: int = 2
    matrix_values: List[List[str]] = [["0" for _ in range(2)] for _ in range(2)]
    constants_values: List[str] = ["0" for _ in range(2)]
    result: str = ""
    solution: List[str] = []
    is_random: bool = False
    use_fractions: bool = True
    graph_data: go.Figure = go.Figure()
    show_graph: bool = False  # Nueva variable para controlar la visualización de la gráfica

    def update_matrix(self):
        self.matrix_values = [["0" for _ in range(self.n)] for _ in range(self.m)]
        self.constants_values = ["0" for _ in range(self.m)]
        self.show_graph = False  # Ocultar la gráfica al actualizar la matriz

    def set_matrix_value(self, i: int, j: int, value: str):
        self.matrix_values[i][j] = value
        self.show_graph = False  # Ocultar la gráfica al cambiar un valor

    def set_constant_value(self, i: int, value: str):
        self.constants_values[i] = value
        self.show_graph = False  # Ocultar la gráfica al cambiar un valor

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
        self.show_graph = self.m == 2 and self.n == 2  # Mostrar la gráfica solo si es un sistema 2x2

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
        self.show_graph = False  # Ocultar la gráfica al limpiar todo
        self.update_graph()

    def update_graph(self):
        if self.m == 2 and self.n == 2:
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
        else:
            self.graph_data = go.Figure()

def github_icon() -> rx.Component:
    return rx.link(
        rx.icon(
            "github",
            size=40,
            color="#808080",
            _hover={"color": "#ffffff"}
        ),
        href="https://github.com/danielbanariba/sistemas-de-ecuaciones",
        position="fixed",
        top="1em",
        right="1em",
        z_index="1000",
        target="_blank",
        rel="noopener noreferrer"
    )

def fraction(numerator: rx.Var, denominator: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.text(numerator, font_size="0.9em"),
        rx.box(height="1px", width="100%", bg="currentColor"),
        rx.text(denominator, font_size="0.9em"),
        align="center",
        spacing="1px",
        display="inline-flex",
    )

def fraction_result(solution: rx.Var) -> rx.Component:
    return rx.hstack(
        rx.foreach(
            solution,
            lambda item: rx.hstack(
                rx.text(item.split(" = ")[0] + " ="),
                rx.cond(
                    item.split(" = ")[1].contains("/"),
                    fraction(
                        item.split(" = ")[1].split("/")[0],
                        item.split(" = ")[1].split("/")[1]
                    ),
                    rx.text(item.split(" = ")[1])
                ),
                margin="0.5em",
            )
        ),
        flex_wrap="wrap",
        justify="center",
        align="center",
    )

def equation_system_graph():
    return rx.plotly(data=State.graph_data, layout={})

def index():
    return rx.box(
        github_icon(),
        rx.center(
            rx.vstack(
                rx.heading("Solucionador de Sistemas de Ecuaciones", size="lg"),
                rx.hstack(
                    rx.input(placeholder="Número de ecuaciones", type="number", value=State.m, on_change=State.set_m),
                    rx.input(placeholder="Número de variables", type="number", value=State.n, on_change=State.set_n),
                ),
                rx.button("Crear matriz", on_click=State.update_matrix),
                rx.vstack(
                    rx.heading("Matriz de coeficientes:", size="md"),
                    rx.foreach(
                        State.matrix_values,
                        lambda row, i: rx.hstack(
                            rx.foreach(
                                row,
                                lambda cell, j: rx.input(
                                    value=cell,
                                    on_change=lambda v: State.set_matrix_value(i, j, v),
                                    width="60px",
                                    placeholder_color="#131821"
                                )
                            )
                        )
                    )
                ),
                rx.vstack(
                    rx.heading("Términos independientes:", size="md"),
                    rx.hstack(
                        rx.foreach(
                            State.constants_values,
                            lambda cell, i: rx.input(
                                value=cell,
                                on_change=lambda v: State.set_constant_value(i, v),
                                width="60px",
                                placeholder_color="#131821"
                            )
                        )
                    )
                ),
                rx.hstack(
                    rx.button("Resolver", on_click=State.solve_system),
                    rx.button("Generar y Resolver Aleatorio", on_click=State.solve_random),
                    rx.button(
                        rx.cond(State.use_fractions, "Cambiar a Decimales", "Cambiar a Fracciones"),
                        on_click=State.toggle_result_format
                    ),
                    rx.button("Limpiar todo", on_click=State.clean_all),
                ),
                rx.text(State.result),
                rx.cond(
                    State.solution,
                    fraction_result(State.solution),
                    rx.text("No hay solución disponible")
                ),
                rx.cond(
                    State.show_graph,  # Cambiado para usar la nueva variable de control
                    equation_system_graph(),
                    rx.text("Resuelva un sistema 2x2 para ver la gráfica")
                ),
                rx.cond(
                    State.is_random,
                    rx.vstack(
                        rx.heading("Matriz de coeficientes generada:", size="md"),
                        rx.foreach(
                            State.matrix_values,
                            lambda row, i: rx.hstack(
                                rx.foreach(
                                    row,
                                    lambda cell, j: rx.text(cell, width="60px", text_align="center")
                                )
                            )
                        ),
                        rx.heading("Términos independientes generados:", size="md"),
                        rx.hstack(
                            rx.foreach(
                                State.constants_values,
                                lambda cell, i: rx.text(cell, width="60px", text_align="center")
                            )
                        ),
                    ),
                ),
                width="100%",
                align_items="center",
                spacing="4",
            ),
            width="100%",
            min_height="100vh",
            padding="4",
        ),
        background_color="#1a202c",
        color="white",
    )

app = rx.App()
app.add_page(index)