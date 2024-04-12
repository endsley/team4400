import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 300

    def display():
        def display_problem():
            display_color_problem_title()
            [(x_00, x_01, y_00, y_01, y_10, y_11,z_00, z_01)] = retrieve_display_variables()
            display_new_line(
                r'''
                Given X = \begin{bmatrix}
                 %d & %d
                \end{bmatrix}

                
                Y = \begin{bmatrix}
                 %d&  %d\\ 
                 %d&  %d\\
                \end{bmatrix},
                
                Z =\begin{bmatrix}
                 %d & %d
                \end{bmatrix}
                
                $XYZ^{\top}$ = $a$. 
                 ''',
                [x_00, x_01, y_00, y_01, y_10, y_11,z_00, z_01])


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:

            [x_00, x_01, y_00, y_01, y_10, y_11,z_00, z_01] = getMultInts(8, -4, 4)
            set_page_variables_for_display([x_00, x_01, y_00, y_01, y_10, y_11,z_00, z_01])
            display_problem()
            def product(x,y,z):
                return np.dot(np.dot(x, y), z.T)
            arr = np.array([
                [x_00, x_01],
            ],
            [[y_00, y_01],
              [y_10, y_11]]
            ,
            [[z_00, z_01]])

            solution = product(arr)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

