import reflex as rx
from resuelvesistema.components.fraction_result import fraction_result
from resuelvesistema.components.github_icon import github_icon
from resuelvesistema.state import State
from resuelvesistema.styles.styles import button_style, equation_system_graph, ondas_effect

def index():
    return rx.box(
        #ondas_effect(),
        github_icon(),
        rx.center(
            rx.vstack(
                rx.heading("Solucionador de Sistemas de Ecuaciones", size="1", text_align="center"),
                rx.vstack(
                    rx.input(
                        placeholder="Número de ecuaciones (1-10)",
                        type_="number",
                        value=State.m,
                        on_change=State.set_m,
                        width="100%",
                        min_="1",
                        max_="10",
                    ),
                    rx.input(
                        placeholder="Número de variables (1-10)",
                        type_="number",
                        value=State.n,
                        on_change=State.set_n,
                        width="100%",
                        min_="1",
                        max_="10",
                    ),
                    rx.cond(
                        State.validation_error,
                        rx.text(
                            State.validation_error,
                            color="red.400",
                            font_size="0.875rem",
                        ),
                    ),
                    rx.button(
                        "Crear matriz",
                        on_click=State.update_matrix,
                        style=button_style,
                        disabled=State.validation_error != "",
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.vstack(
                    rx.heading("Matriz de coeficientes:", size="2"),
                    rx.box(
                        # Crea la matrix segun los inputs de m y n
                        rx.foreach(
                            State.matrix_values,
                            lambda row, i: rx.hstack(
                                rx.foreach(
                                    row,
                                    lambda cell, j: rx.input(
                                        value=cell,
                                        on_change=lambda v: State.set_matrix_value(i, j, v),
                                        width="100%",
                                    ),
                                ),
                                padding_bottom="0.5em",
                                spacing="2",
                                width="100%",
                            ),
                        ),
                        overflow_x="auto",
                        width="100%",
                    ),
                ),
                rx.vstack(
                    rx.heading("Términos independientes:", size="2"),
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
                    rx.button(
                        rx.cond(
                            State.is_solving,
                            rx.hstack(
                                rx.spinner(size="1"),
                                rx.text("Resolviendo..."),
                                spacing="2",
                            ),
                            rx.text("Resolver"),
                        ),
                        on_click=State.solve_system,
                        style=button_style,
                        disabled=State.is_solving,
                    ),
                    rx.button(
                        "Generar y Resolver Aleatorio",
                        on_click=State.solve_random,
                        style=button_style,
                        disabled=State.is_solving,
                    ),
                    rx.button(
                        rx.cond(
                            State.use_fractions,
                            "Cambiar a Decimales",
                            "Cambiar a Fracciones"
                        ),
                        on_click=State.toggle_result_format,
                        style=button_style,
                    ),
                    rx.button(
                        "Limpiar todo",
                        on_click=State.clean_all,
                        style=button_style
                    ),
                    spacing="2",
                    width="100%",
                ),
                rx.text(
                    State.result,
                    font_weight="bold",
                    color=rx.cond(
                        State.result.contains("Error"),
                        "red.400",
                        rx.cond(
                            State.result.contains("encontrada"),
                            "green.400",
                            "yellow.400"
                        )
                    )
                ),
                rx.cond(
                    State.solution,
                    fraction_result(State.solution),
                    rx.text("No hay solución disponible")
                ),
                # Mostrar análisis del sistema
                rx.cond(
                    State.equations_display.length() > 0,
                    rx.vstack(
                        # Sistema de ecuaciones
                        rx.box(
                            rx.heading("Sistema de Ecuaciones", size="3", margin_bottom="0.5em"),
                            rx.vstack(
                                rx.foreach(
                                    State.equations_display,
                                    lambda eq: rx.text(
                                        eq,
                                        font_family="monospace",
                                        font_size="1rem",
                                        padding="0.25em 0",
                                    )
                                ),
                                spacing="1",
                                align_items="start",
                            ),
                            background_color="#2d3748",
                            padding="1em",
                            border_radius="0.5em",
                            width="100%",
                        ),
                        # Representación matricial
                        rx.box(
                            rx.heading("Representación Matricial: Ax = b", size="3", margin_bottom="0.5em"),
                            rx.hstack(
                                # Matriz A
                                rx.vstack(
                                    rx.text("A", font_weight="bold", color="blue.300"),
                                    rx.box(
                                        rx.vstack(
                                            rx.foreach(
                                                State.matrix_A_display,
                                                lambda row: rx.hstack(
                                                    rx.foreach(
                                                        row,
                                                        lambda val: rx.box(
                                                            rx.text(val, font_family="monospace"),
                                                            padding="0.25em 0.5em",
                                                            min_width="3em",
                                                            text_align="center",
                                                        )
                                                    ),
                                                    spacing="1",
                                                )
                                            ),
                                            spacing="1",
                                        ),
                                        border_left="3px solid",
                                        border_right="3px solid",
                                        border_color="blue.400",
                                        padding="0.5em",
                                    ),
                                    align_items="center",
                                ),
                                rx.text("·", font_size="1.5em", font_weight="bold"),
                                # Vector x
                                rx.vstack(
                                    rx.text("x", font_weight="bold", color="green.300"),
                                    rx.box(
                                        rx.vstack(
                                            rx.foreach(
                                                State.variables_list,
                                                lambda var: rx.text(var, font_family="monospace", padding="0.25em")
                                            ),
                                            spacing="1",
                                        ),
                                        border_left="3px solid",
                                        border_right="3px solid",
                                        border_color="green.400",
                                        padding="0.5em",
                                    ),
                                    align_items="center",
                                ),
                                rx.text("=", font_size="1.5em", font_weight="bold"),
                                # Vector b
                                rx.vstack(
                                    rx.text("b", font_weight="bold", color="orange.300"),
                                    rx.box(
                                        rx.vstack(
                                            rx.foreach(
                                                State.vector_b_display,
                                                lambda val: rx.text(val, font_family="monospace", padding="0.25em")
                                            ),
                                            spacing="1",
                                        ),
                                        border_left="3px solid",
                                        border_right="3px solid",
                                        border_color="orange.400",
                                        padding="0.5em",
                                    ),
                                    align_items="center",
                                ),
                                spacing="3",
                                justify_content="center",
                                align_items="center",
                            ),
                            background_color="#2d3748",
                            padding="1em",
                            border_radius="0.5em",
                            width="100%",
                        ),
                        # Análisis de rangos
                        rx.box(
                            rx.heading("Análisis del Sistema", size="3", margin_bottom="0.5em"),
                            rx.vstack(
                                rx.hstack(
                                    rx.badge("Rango(A)", color_scheme="blue"),
                                    rx.text("=", font_weight="bold"),
                                    rx.badge(State.rank_A, color_scheme="blue", variant="solid"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.badge("Rango(A|b)", color_scheme="purple"),
                                    rx.text("=", font_weight="bold"),
                                    rx.badge(State.rank_Ab, color_scheme="purple", variant="solid"),
                                    spacing="2",
                                ),
                                rx.hstack(
                                    rx.badge("Variables", color_scheme="green"),
                                    rx.text("=", font_weight="bold"),
                                    rx.badge(State.num_variables, color_scheme="green", variant="solid"),
                                    spacing="2",
                                ),
                                spacing="2",
                                align_items="start",
                            ),
                            background_color="#2d3748",
                            padding="1em",
                            border_radius="0.5em",
                            width="100%",
                        ),
                        # Conclusión
                        rx.box(
                            rx.heading("Conclusión", size="3", margin_bottom="0.5em"),
                            rx.text(
                                State.conclusion_text,
                                font_size="0.95rem",
                                line_height="1.5",
                            ),
                            background_color=rx.cond(
                                State.result.contains("Única"),
                                "#22543d",
                                rx.cond(
                                    State.result.contains("Inconsistente"),
                                    "#742a2a",
                                    "#744210"
                                )
                            ),
                            padding="1em",
                            border_radius="0.5em",
                            width="100%",
                        ),
                        spacing="3",
                        width="100%",
                    ),
                ),
                rx.cond(
                    State.show_graph,
                    rx.center(
                        equation_system_graph(),
                    ),
                    rx.text("Resuelva un sistema 2x2 o 3x3 para ver la gráfica")
                ),
                padding_top="1em",
                width="100%",
                max_width="400px",
                align_items="center",
                spacing="4",
                padding="4",
            ),
            width="100%",
            min_height="100vh",
            padding_bottom="4em",
        ),
        background_color="#1a202c",
        color="white",
    )

app = rx.App()
app.add_page(index)