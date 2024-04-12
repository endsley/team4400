import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 300

    def display():
        def display_problem():
            display_color_problem_title()
            rand_x = retrieve_display_variables()
            rand_x = np.array(rand_x).reshape(2, 2)
            matrix_str = ''
            for row in rand_x:
                matrix_str += ' & '.join([str(x) for x in row]) + r'\\'
            matrix_str = matrix_str[:-2]
            display_new_line(r''' $\left\langle\begin{bmatrix}%d\end{bmatrix} ,  \begin{bmatrix}%d\end{bmatrix}\right\rangle$ = $a$. What is $a$?''', (matrix_str, matrix_str))


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            [x_00, x_01, x_10, x_11] = getMultInts(4, -4, 4)
            set_page_variables_for_display([x_00, x_01, x_10, x_11])
            display_problem()
            def inner_product(x):
                return np.trace(np.dot(x.T, x))
            arr = np.array([
                [x_00, x_01],
                [x_10, x_11]
            ])
            solution = inner_product(arr)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

