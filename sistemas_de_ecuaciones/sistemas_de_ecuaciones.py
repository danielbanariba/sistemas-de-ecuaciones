import reflex as rx
import numpy as np
from typing import List
from fractions import Fraction
from sistemas_de_ecuaciones.components.github_icon import github_icon
from sistemas_de_ecuaciones.components.fraction_result import fraction_result
from sistemas_de_ecuaciones.state import State

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