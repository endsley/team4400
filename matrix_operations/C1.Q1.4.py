from utils import *
import numpy as np

if __name__ == "__main__":
    n_sec = 100

    def generate_random_matrix_using_getMultInts(rows, cols, min_val, max_val):
        # Replaces generate_random_matrix to use getMultInts for generating random numbers
        matrix = []
        for _ in range(rows):
            # Each call to getMultInts will get a row's worth of integers
            row = getMultInts(cols, min_val, max_val)
            matrix.append(row)
        return np.array(matrix)

    def matrix_to_latex(matrix):
        if matrix.ndim == 1:
            matrix = matrix[:, None]  # Convert 1D array to column vector
        return r'\begin{bmatrix}' + r' \\ '.join(
            ' & '.join(str(cell) for cell in row) for row in matrix) + r'\end{bmatrix}'

    def display_matrix_question_new_problem():
        def define_matrices():
            # Modify the matrix generation to use the new function
            y = generate_random_matrix_using_getMultInts(3, 1, 0, 5)
            return y

        def display_problem(y):
            display_color_problem_title()
            y_latex = matrix_to_latex(y)
            display_new_line(
                r'''Given a vector with random elements:''')
            display_new_line(
                r'''$y = %s$.''' % y_latex)
            display_new_line(
                r'''Calculate $y \otimes y + I$ where $I$ is the identity matrix of appropriate size.
                Enter the sum of all elements of the resulting matrix.''')

        def matrix_solution(y):
            y_outer_y = np.outer(y, y)  # Outer product
            identity_matrix = np.eye(y.shape[0])  # Identity matrix
            result_matrix = y_outer_y + identity_matrix
            return np.sum(result_matrix)  # Sum of all elements of the resulting matrix

        y = define_matrices()  # Define the vector with randomness

        solution = matrix_solution(y)

        if problem_has_been_answered():
            display_problem(y)
            params = display_solutions()
        else:
            display_problem(y)
            params = problem_display_ending(solution, 'number')

            # Preview mode for checking the solution before submission
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write(f"Solution is: {solution}")
        return params

    standard_problem_page(n_sec, display_matrix_question_new_problem)
