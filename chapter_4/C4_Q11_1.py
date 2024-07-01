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
                Assume that the function is a parabola where
$$
f(x)=a x^2+b x+c .
$$
 What is $a$ with closed-form solution?
 If there is no solution, just enter the number -10000000.
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

            # Calculate the estimated solution
            x_values = np.array([x00, x10, x20, x30])
            y_values = np.array([x01, x11, x21, x31])

            # Construct the design matrix X
            X = np.vstack([x_values**2, x_values, np.ones(len(x_values))]).T

            # Compute (X^T X)^(-1) X^T y
            try:
                beta = np.linalg.inv(X.T @ X) @ X.T @ y_values
                a, b, c = beta
                solution = a
            except np.linalg.LinAlgError:
                solution = -10000000

            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)
