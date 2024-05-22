import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 150


    def display():
        def display_problem():
            display_color_problem_title()
            (x00, x01, x10, x11, x20, x21, x30, x31) = retrieve_display_variables()
            display_new_line(
                r''' 
                Given the following data:
                '''
            )
            display_new_line(
                r''' 
                $\begin{bmatrix}
                x_{1} & x_{2} \\
                %d & %d \\
                %d & %d \\
                %d & %d \\
                %d & %d
                \end{bmatrix}$
                ''',
                (x00, x01, x10, x11, x20, x21, x30, x31)
            )
            display_new_line(
                r''' 
                Transform the data using the feature map: $\phi_6(x) =  1$. 
                What is the first element in $\phi_6(x)$?
                '''
            )

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # get values for matrix and display
            mat_vals = getMultInts(8, -4, 4)
            (x00, x01, x10, x11, x20, x21, x30, x31) = mat_vals
            set_page_variables_for_display([x00, x01, x10, x11, x20, x21, x30, x31])
            display_problem()

            # calculate the estimated solution
            solution = 1
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params


    standard_problem_page(n_sec, display)