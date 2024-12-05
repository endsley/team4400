import streamlit as st
import numpy as np
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def matrix_to_latex(matrix):
            if matrix.ndim == 1:
                matrix = matrix[:, None]  # Convert 1D array to column vector
            return r'\begin{bmatrix}' + r' \\ '.join(
                ' & '.join(str(cell) for cell in row) for row in matrix) + r'\end{bmatrix}'

        def display_problem():
            display_color_problem_title()
            # Retrieve the matrices and vectors from the session state
            x, y, Y = retrieve_display_variables()
            x_latex = matrix_to_latex(x)
            y_latex = matrix_to_latex(y)
            Y_latex = matrix_to_latex(Y)
            display_new_line(r'''Given vectors and matrices with random elements:''')
            display_new_line(r'''$x = %s$, $y = %s$, and $Y = %s$ are given.''' % (x_latex, y_latex, Y_latex))
            display_new_line(r'''Calculate $Y^{\top}(x \odot y) + \langle x, y \rangle$. Only enter the first element of the resulting vector.''')

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # Generate random integers for the matrices and vectors using getMultInts
            random_values = getMultInts(15, -5, 5)  # Total 15 values to distribute among x, y, and Y
            x = np.array(random_values[:3]).reshape(3, 1)
            y = np.array(random_values[3:6]).reshape(3, 1)
            Y = np.array(random_values[6:]).reshape(3, 3)
            set_page_variables_for_display([x, y, Y])
            display_problem()

            def matrix_solution():
                # Retrieve the matrices and vectors from the session state
                x, y, Y = retrieve_display_variables()
                x_dot_y = np.multiply(x, y)  # Element-wise multiplication
                Y_transpose = Y.T
                result_Y_transpose_x_dot_y = np.dot(Y_transpose, x_dot_y)
                dot_product_x_y = np.dot(x.T, y)[0][0]  # Ensure dot product is scalar
                final_result = result_Y_transpose_x_dot_y + dot_product_x_y
                return final_result[0][0]

            solution = matrix_solution()
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)
