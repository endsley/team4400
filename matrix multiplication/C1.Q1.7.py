import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def generate_random_matrix(rows, cols, min_val, max_val):
        # Generates a matrix with random integers of the specified size
        return np.random.randint(min_val, max_val + 1, size=(rows, cols))

    def display_matrix_question():


        def define_matrices():
            x = generate_random_matrix(3, 1, 0, 5)
            y = generate_random_matrix(3, 1, 0, 5)
            return x, y

        def matrix_to_latex(matrix):
            if matrix.ndim == 1:
                matrix = matrix[:, None]  # Convert 1D array to column vector
            return r'\begin{bmatrix}' + r' \\ '.join(
                ' & '.join(str(cell) for cell in row) for row in matrix) + r'\end{bmatrix}'

        def display_problem(x, y):
            # Convert numpy arrays to LaTeX bmatrix format.

            x_latex = matrix_to_latex(x)
            y_latex = matrix_to_latex(y)
            
            display_new_line(
                r'''Given vectors with random elements:''')
            display_new_line(
                r'''$x = %s$ and $y = %s$ are vectors.''' % (
                    x_latex, y_latex))
            display_new_line(
                r'''Calculate $\langle y, x \rangle$.''')

        if problem_has_been_answered():
            display_problem(x, y)
            params = display_solutions()
        else:
            [random1_val1, random1_val2, random1_val3, random2_val1, random2_val2, random2_val3] = getMultInts(6, 1, 3)
            set_page_variables_for_display([random1_val1, random1_val2, random1_val3, random2_val1, random2_val2, random2_val3])
            x = np.array([[random1_val1],
                          [random1_val2],
                          [random1_val3]])
            y = np.array([[random2_val1],
                          [random2_val2],
                          [random2_val3]])
            display_problem(x, y)
            
            def inner_product(x, y):
                return y.T.dot(x)
            
            solution = inner_product(x, y).item()
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display_matrix_question)