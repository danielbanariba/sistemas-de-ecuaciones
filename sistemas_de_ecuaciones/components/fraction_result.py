import reflex as rx
from sistemas_de_ecuaciones.components.fraction import fraction

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