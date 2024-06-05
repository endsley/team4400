import streamlit as st
import numpy as np
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()
            [c, d, n, a, b] = retrieve_display_variables()
            display_new_line(r'''Calculate the integral of $f(x) = %dx^{%d} + %d$ over the interval $[%d, %d]$''', (c, n, d, a, b))

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # We are now going to use a common range for all parameters, here we pick a range that potentially fits all:
            [c, d, n, a, b] = getMultInts(5, 0, 10)

            c = (c % 5) + 1   # Coefficient of x^n, from 1 to 5
            d = d            # Constant term, 0 to 10 (since the range 0-11 is close enough)
            n = (n % 4) + 2  # Power of x, from 2 to 5
            a = 0            # Lower bound of the integral fixed to 0
            b = (b % 5) + 1  # Upper bound of the integral, from 1 to 5
            set_page_variables_for_display([c, d, n, a, b])
            display_problem()

            def integral_solution():
                c, d, n, a, b = retrieve_display_variables()
                integral_c = (c / (n + 1)) * (b ** (n + 1) - a ** (n + 1))  # Integral of cx^n over [a, b]
                integral_d = d * (b - a)  # Integral of d over [a, b]
                return integral_c + integral_d

            solution = integral_solution()
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)
