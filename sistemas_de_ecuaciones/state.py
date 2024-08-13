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
    solution: List[str] = []
    is_random: bool = False
    use_fractions: bool = True

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