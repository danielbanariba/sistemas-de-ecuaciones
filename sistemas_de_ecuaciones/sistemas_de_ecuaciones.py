import reflex as rx
from sistemas_de_ecuaciones.components.fraction_result import fraction_result
from sistemas_de_ecuaciones.components.github_icon import github_icon
from sistemas_de_ecuaciones.state import State

def equation_system_graph():
    return rx.plotly(
        data=State.graph_data,
        layout={
            "width": "100%",
            "height": "100%",
        },
        config={"responsive": True}
    )

def button_style():
    return {
        "width": "100%",
        "bg": "#4299E1",
        "color": "white",
        "_hover": {"bg": "#3182CE"},
    }

def index():
    return rx.box(
        github_icon(),
        rx.center(
            rx.vstack(
                rx.heading("Solucionador de Sistemas de Ecuaciones", size="lg", text_align="center"),
                rx.vstack(
                    rx.input(placeholder="Número de ecuaciones", type_="number", value=State.m, on_change=State.set_m, width="100%"),
                    rx.input(placeholder="Número de variables", type_="number", value=State.n, on_change=State.set_n, width="100%"),
                    rx.button("Crear matriz", on_click=State.update_matrix, style=button_style()),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading("Matriz de coeficientes:", size="md"),
                    rx.box(
                        rx.foreach(
                            State.matrix_values,
                            lambda row, i: rx.hstack(
                                rx.foreach(
                                    row,
                                    lambda cell, j: rx.input(
                                        value=cell,
                                        on_change=lambda v: State.set_matrix_value(i, j, v),
                                        width="100%",
                                    )
                                ),
                                padding_bottom="0.5em",
                                spacing="2",
                                width="100%",
                            )
                        ),
                        overflow_x="auto",
                        width="100%",
                    )
                ),
                rx.vstack(
                    rx.heading("Términos independientes:", size="md"),
                    rx.box(
                        rx.hstack(
                            rx.foreach(
                                State.constants_values,
                                lambda cell, i: rx.input(
                                    value=cell,
                                    on_change=lambda v: State.set_constant_value(i, v),
                                    width="100%",
                                )
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        overflow_x="auto",
                        width="100%",
                    )
                ),
                rx.vstack(
                    rx.button("Resolver", on_click=State.solve_system, style=button_style()),
                    rx.button("Generar y Resolver Aleatorio", on_click=State.solve_random, style=button_style()),
                    rx.button(
                        rx.cond(State.use_fractions, "Cambiar a Decimales", "Cambiar a Fracciones"),
                        on_click=State.toggle_result_format,
                        style=button_style()
                    ),
                    rx.button("Limpiar todo", on_click=State.clean_all, style=button_style()),
                    spacing="2",
                    width="100%",
                ),
                rx.text(State.result),
                rx.cond(
                    State.solution,
                    fraction_result(State.solution),
                    rx.text("No hay solución disponible")
                ),
                rx.cond(
                    State.show_graph,
                    rx.center(
                        equation_system_graph(),
                    ),
                    rx.text("Resuelva un sistema 2x2 o 3x3 para ver la gráfica")
                ),
                width="100%",
                max_width="400px",
                align_items="center",
                spacing="4",
                padding="4",
            ),
            width="100%",
            min_height="100vh",  # Cambiado de height a min_height
            padding_bottom="4em",  # Añade un padding en la parte inferior
        ),
        background_color="#1a202c",
        color="white",
    )

app = rx.App()
app.add_page(index)