from utils import *
import numpy as np


if __name__ == "__main__":
    n_sec = 100


    def generate_random_matrix(rows, cols, min_val, max_val):
        # Generates a matrix with random integers of the specified size
        return np.random.randint(min_val, max_val + 1, size=(rows, cols))


    def display_matrix_question():

        def define_matrices():
            x = generate_random_matrix(3, 1, 0, 5)
            y = generate_random_matrix(3, 1, 0, 5)
            Y = generate_random_matrix(3, 3, -5, 5)
            return x, y, Y

        def matrix_to_latex(matrix):
            if matrix.ndim == 1:
                matrix = matrix[:, None]  # Convert 1D array to column vector
            return r'\begin{bmatrix}' + r' \\ '.join(
                ' & '.join(str(cell) for cell in row) for row in matrix) + r'\end{bmatrix}'



        def display_problem(x, y, Y):
            # Convert numpy arrays to LaTeX bmatrix format.

            x_latex = matrix_to_latex(x)
            y_latex = matrix_to_latex(y)
            Y_latex = matrix_to_latex(Y)

            display_new_line(
                r'''Given vectors and matrices with random elements:''')
            display_new_line(
                r'''$x = %s$ and $y = %s$ are vectors, and $Y = %s$ is a matrix.''' % (
                    x_latex, y_latex, Y_latex))
            display_new_line(
                r'''Calculate $Y^{\top}(x \odot y)+\langle x, y\rangle$. 
                And only enter the first element of the resulting vector.''')


        def matrix_solution(x, y, Y):
            x_dot_y = np.multiply(x, y)  # Element-wise multiplication
            Y_transpose = Y.T
            result_Y_transpose_x_dot_y = np.dot(Y_transpose, x_dot_y)
            dot_product_x_y = np.dot(x.T, y)
            # Ensure final result is a column vector for consistency
            final_result = result_Y_transpose_x_dot_y + dot_product_x_y

            # Return the first element of the resulting vector
            return final_result[0][0]

        x, y, Y = define_matrices()  # Define the matrices and vectors with randomness

        solution = matrix_solution(x, y, Y)

        if problem_has_been_answered():
            display_problem(x, y, Y)
            params = display_solutions()
        else:
            display_problem(x, y, Y)
            params = problem_display_ending(solution, 'number')

            # Preview mode for checking the solution before submission
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write(f"Solution is: {solution}")
        return params




    standard_problem_page(n_sec, display_matrix_question)
