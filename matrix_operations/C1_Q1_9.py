#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import time

if __name__ == "__main__":
    n_sec = 60


def display():
    #	Define this function for new problem
    def display_problem():
        display_color_problem_title()

        #	parts where you change
        [a, b, c, d, e, f, g, h,i,j,k,l, v] = retrieve_display_variables()
        display_new_line(r''' X =  $$ \begin{bmatrix}
                        %d & %d \\%d & %d\end{bmatrix} $$ , Y = $$  \begin{bmatrix}%d & %d \\%d & %d
                    \end{bmatrix} $$, Y = $$  \begin{bmatrix}%d & %d \\%d & %d
                    \end{bmatrix} $$''',(a, b, c, d, e, f, g, h,i,j,k,l))
        display_new_line(r'''$$ XYZ^{\top} =  \begin{bmatrix} a & b \\ c & d \\ e & f
\end{bmatrix} $$, What is $$%s$$ ?''',(v))

    # -------------------------------------------------------------------

    if problem_has_been_answered():
        display_problem()
        params = display_solutions()
    else:
        # generate random data
        [a, b, c, d, e, f, g, h, i,j, k, l] = getMultInts(12, -4, 4)
        v = getInt(0,4,'v')
        L = ['a', 'b', 'c', 'd']

        # define key variables and display the problem
        set_page_variables_for_display([a, b, c, d, e, f, g, h,i,j,k,l ,L[v]])
        display_problem()

        # define the solution
        X = np.array([[a, b],
                     [c, d]])
        Y = np.array([[e, f],
                     [g, h]])
        Z = np.array([[i, j],
                     [k, l]])
        solution = (X.dot(Y).dot(Z.T)) [v//2, v%2].item()
        params = problem_display_ending(solution, 'number')

        if 'preview' in st.session_state and st.session_state['preview'] == 1:
            st.write("Solution is: " + str(solution))

    return params

standard_problem_page(n_sec, display)