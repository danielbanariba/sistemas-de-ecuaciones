import reflex as rx

def fraction(numerator: rx.Var, denominator: rx.Var) -> rx.Component:
    return rx.vstack(
        rx.text(numerator, font_size="0.9em"),
        rx.box(height="1px", width="100%", bg="currentColor"),
        rx.text(denominator, font_size="0.9em"),
        align="center",
        spacing="1px",
        display="inline-flex",
    )