import streamlit as st
import numpy as np
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem(c, d, n, a, b):
            display_color_problem_title()
            display_new_line(r'''Calculate the integral of $f(x) = %dx^{%d} + %d$ over the interval $[%d, %d]$''', (c, n, d, a, b))

        if problem_has_been_answered():
            c, d, n, a, b = retrieve_display_variables()
            display_problem(c, d, n, a, b)
            params = display_solutions()
        else:
            c = np.random.randint(1, 6)  # Coefficient of x^n
            d = np.random.randint(0, 11)  # Constant term
            n = np.random.randint(2, 6)  # Power of x
            a = 0  # Lower bound of the integral
            b = np.random.randint(1, 6)  # Upper bound of the integral
            set_page_variables_for_display([c, d, n, a, b])
            display_problem(c, d, n, a, b)
            def integral_solution(c, d, n, a, b):
                integral_c = (c / (n + 1)) * (b ** (n + 1) - a ** (n + 1))  # Integral of cx^n over [a, b]
                integral_d = d * (b - a)  # Integral of d over [a, b]
                return integral_c + integral_d
            solution = integral_solution(c, d, n, a, b)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)
