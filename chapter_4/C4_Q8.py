import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 150

    def display():
        def display_problem():
            display_color_problem_title()
            (x00, x01, x10, x11, x20, x21) = retrieve_display_variables()
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
                %d & %d
                \end{bmatrix}$
                ''',
                (x00, x01, x10, x11, x20, x21)
            )
            display_new_line(
                r'''
                We want to approximate this data using the function
$$
f(x)=w_1 x^2+w_2 x .
$$
 What is $w_1 + w_2$ using the closed-form regression method?
                '''
            )

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # get values for matrix and display
            mat_vals = getMultInts(6, -10, 10)
            (x00, x01, x10, x11, x20, x21) = mat_vals
            set_page_variables_for_display([x00, x01, x10, x11, x20, x21])
            display_problem()

            # Calculate the estimated solution
            x_values = np.array([x00, x10, x20])
            y_values = np.array([x01, x11, x21])

            # Construct the design matrix X
            X = np.vstack([x_values**2, x_values]).T

            # Compute (X^T X)^(-1) X^T y
            try:
                beta = np.linalg.inv(X.T @ X) @ X.T @ y_values
                w1, w2 = beta
                solution = w1 + w2
            except np.linalg.LinAlgError:
                solution = -10000000

            params = problem_display_ending(solution, 'value')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)
