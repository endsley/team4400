import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 900

    def display():
        def display_problem():
            display_color_problem_title()
            rand_nums = retrieve_display_variables()
            display_new_line(
                r''' 
                Given $f(x) = ||x||_1 + ||x||_2^2 + ReLU(w^Tx) + x^TAx$ and the following matrices: $\\ \\$
                    $
                    \frac{df}{dx}(a) = \begin{bmatrix}
                        y \\ z
                    \end{bmatrix}\space\space
                    a = \begin{bmatrix}
                        %d \\ %d
                    \end{bmatrix},\space\space 
                    w = \begin{bmatrix}
                        %d \\ %d
                    \end{bmatrix},\space\space       
                    A = \begin{bmatrix}
                        %d & %d \\ %d & %d
                    \end{bmatrix}$.$\\ \\$
                What is the value of y (rounded to 1 decimal place)? 
                ''',
                # tuple of each number in matrix
                tuple(rand_nums)
                )


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # get values for matrix and display
            mat_vals = getMultInts(8, -5, 5)
            (a0, a1, w0, w1, A00, A01, A10, A11) = mat_vals
            set_page_variables_for_display([a0, a1, w0, w1, A00, A01, A10, A11])
            display_problem()

            # define variables
            (a0, a1, w0, w1, A00, A01, A10, A11) = mat_vals
            a = np.array([
                [a0],
                [a1]
            ])

            w = np.array([
                [w0],
                [w1]
            ])

            A = np.array([
                [A00, A01],
                [A10, A11]
            ])

            # get solution
            # L1 + L2 + ReLU(wTx) + xTAx
            l1_drv = np.sign(a)
            l2_drv = a / np.linalg.norm(a, ord=2)
            wTx = np.dot(w.T, a)
            relu_drv = 0
            if wTx > 0:
                relu_drv = a
            xTAx_drv = np.dot(A.T + A, a)
            solution = l1_drv + l2_drv + relu_drv + xTAx_drv
            solution = round(solution.reshape(2, 1)[0, 0], 1)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

