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
                    x & y \\
                    1 & 1 \\
                    2 & 1 \\
                    1.5 & 0 \\
                    3 & 2 \\
                \end{bmatrix}$
                ''',
                (x00, x01, x10, x11, x20, x21, x30, x31)
            )
            display_new_line(
                r''' 
                Assume that the function is a parabola where 
                $\begin{equation*}
                f(x) = a x^2 + b x + c.
                \end{equation*}$
                '''
            )
            display_new_line(
                r'''
                Given the initial values for GD as $a_0 = 1, b_0 = 1, c_0 = 1$, and step size $\eta=0.1$.
                $\begin{enumerate}
                \item What is $a, b $ or $c$ after 1 GD step?
                \end{enumerate}$
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
            solution = x01 ###Have to change this to reflect it being a b or c
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params


    standard_problem_page(n_sec, display)