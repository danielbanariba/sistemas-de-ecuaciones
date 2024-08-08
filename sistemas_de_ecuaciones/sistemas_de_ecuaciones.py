import reflex as rx
import numpy as np
from typing import List

class State(rx.State):
    m: int = 2
    n: int = 2
    matrix_values: List[List[float]] = [[0.0 for _ in range(2)] for _ in range(2)]
    constants_values: List[float] = [0.0 for _ in range(2)]
    result: str = ""
    is_random: bool = False

    def update_matrix(self):
        self.matrix_values = [[0.0 for _ in range(self.n)] for _ in range(self.m)]
        self.constants_values = [0.0 for _ in range(self.m)]

    def set_matrix_value(self, i: int, j: int, value: str):
        try:
            self.matrix_values[i][j] = float(value)
        except ValueError:
            pass  # Ignorar entradas no válidas

    def set_constant_value(self, i: int, value: str):
        try:
            self.constants_values[i] = float(value)
        except ValueError:
            pass  # Ignorar entradas no válidas

    def solve_system(self):
        try:
            matrix = np.array(self.matrix_values, dtype=float)
            constants = np.array(self.constants_values, dtype=float)
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
                    self.result = "Solución:\n" + "\n".join([f"x{i+1} = {sol:.4f}" for i, sol in enumerate(solution)])
                except np.linalg.LinAlgError:
                    self.result = "El sistema no tiene una solución única (matriz singular)."
        except ValueError:
            self.result = "Error: Por favor, ingrese números válidos en todas las celdas."

    def solve_random(self):
        self.is_random = True
        coefficients = np.random.randint(-10, 11, size=(self.m, self.n)).astype(float)
        constants = np.random.randint(-10, 11, size=(self.m,)).astype(float)
        
        self.matrix_values = coefficients.tolist()
        self.constants_values = constants.tolist()
        
        self.solve_system()

def index():
    return rx.center(  # Envolvemos todo el contenido en rx.center
        rx.vstack(
            rx.heading("Solucionador de Sistemas de Ecuaciones"),
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
                                value=str(cell),
                                on_change=lambda v: State.set_matrix_value(i, j, v),
                                type="number",
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
                            value=str(cell),
                            on_change=lambda v: State.set_constant_value(i, v),
                            type="number",
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
            width="100%",  # Asegura que el vstack ocupe todo el ancho disponible
            align_items="center",  # Centra los elementos horizontalmente dentro del vstack
        ),
        width="100%",  # Asegura que el center ocupe todo el ancho de la página
        height="100vh",  # Hace que el center ocupe toda la altura de la ventana
    )

app = rx.App()
app.add_page(index)