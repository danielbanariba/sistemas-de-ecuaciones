import reflex as rx
import numpy as np
from typing import List
from fractions import Fraction

class State(rx.State):
    m: int = 2
    n: int = 2
    matrix_values: List[List[str]] = [["0" for _ in range(2)] for _ in range(2)]
    constants_values: List[str] = ["0" for _ in range(2)]
    result: str = ""
    is_random: bool = False
    is_dark_theme: bool = False

    def update_matrix(self):
        self.matrix_values = [["0" for _ in range(self.n)] for _ in range(self.m)]
        self.constants_values = ["0" for _ in range(self.m)]

    def set_matrix_value(self, i: int, j: int, value: str):
        self.matrix_values[i][j] = value

    def set_constant_value(self, i: int, value: str):
        self.constants_values[i] = value

    def parse_fraction(self, value: str) -> float:
        try:
            return float(Fraction(value))
        except ValueError:
            return 0.0

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
            elif rank_A < A.shape[1]:
                self.result = "El sistema tiene infinitas soluciones."
            else:
                try:
                    solution = np.linalg.solve(A, b)
                    self.result = "Solución:\n" + "\n".join([f"x{i+1} = {Fraction(sol).limit_denominator()}" for i, sol in enumerate(solution)])
                except np.linalg.LinAlgError:
                    self.result = "El sistema no tiene una solución única (matriz singular)."
        except ValueError:
            self.result = "Error: Por favor, ingrese números o fracciones válidas en todas las celdas."

    def solve_random(self):
        self.is_random = True
        coefficients = np.random.randint(-10, 11, size=(self.m, self.n)).astype(float)
        constants = np.random.randint(-10, 11, size=(self.m,)).astype(float)
        
        self.matrix_values = [[str(Fraction(val).limit_denominator()) for val in row] for row in coefficients.tolist()]
        self.constants_values = [str(Fraction(val).limit_denominator()) for val in constants.tolist()]
        
        self.solve_system()

    def toggle_theme(self):
        self.is_dark_theme = not self.is_dark_theme

def index():
    return rx.box(
        rx.vstack(
            rx.flex(
                rx.box(
                    rx.heading("Solucionador de Sistemas de Ecuaciones", size="lg"),
                    width="100%",
                    text_align="center",
                ),
                rx.box(
                    rx.button(
                        rx.cond(
                            State.is_dark_theme,
                            rx.icon(tag="sun"),
                            rx.icon(tag="moon")
                        ),
                        on_click=State.toggle_theme,
                        variant="ghost",
                    ),
                    position="absolute",
                    right="1em",
                    top="1em",
                ),
                width="100%",
                position="relative",
                padding_y="4",
            ),
            rx.hstack(
                rx.input(placeholder="Número de ecuaciones", type_="number", value=State.m, on_change=State.set_m),
                rx.input(placeholder="Número de variables", type_="number", value=State.n, on_change=State.set_n),
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
                        )
                    )
                )
            ),
            rx.button("Resolver", on_click=State.solve_system),
            rx.button("Generar y Resolver Aleatorio", on_click=State.solve_random),
            rx.text(State.result),
            rx.cond(
                State.is_random,
                rx.vstack(
                    rx.text("Matriz de coeficientes generada:"),
                    rx.text(State.matrix_values),
                    rx.text("Términos independientes generados:"),
                    rx.text(State.constants_values),
                ),
            ),
            width="100%",
            align_items="center",
            spacing="4",
        ),
        width="100%",
        min_height="100vh",
        padding="4",
        background_color=rx.cond(State.is_dark_theme, "#1a202c", "white"),
        color=rx.cond(State.is_dark_theme, "white", "black"),
    )

app = rx.App()
app.add_page(index)