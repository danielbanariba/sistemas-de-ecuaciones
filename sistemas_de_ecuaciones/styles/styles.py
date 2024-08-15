import reflex as rx
from ..state import State

def equation_system_graph():
    return rx.plotly(
        data=State.graph_data,
        layout={
            "width": "100%",
            "height": "100%",
        },
        config={"responsive": True}
    )

button_style = {
    "width": "100%",
    "bg": "#4299E1",
    "color": "white",
    "_hover": {"bg": "#3182CE"},
}