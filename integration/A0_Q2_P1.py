import streamlit as st
import numpy as np
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()
            # Retrieve the variables needed for displaying the problem
            [c, d, n, a, b] = retrieve_display_variables()
            display_new_line(r'''Calculate the integral of $f(x) = %dx^{%d} + %d$ over the interval $[%d, %d]$''', (c, n, d, a, b))

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # Generate random values for the coefficients, constant term, power of x, and bounds of integration
            c = np.random.randint(1, 6)  # Coefficient of x^n
            d = np.random.randint(0, 11)  # Constant term
            n = np.random.randint(2, 6)  # Power of x
            a = 0  # Lower bound of the integral
            b = np.random.randint(1, 6)  # Upper bound of the integral
            # Store these variables for later retrieval
            set_page_variables_for_display([c, d, n, a, b])
            display_problem()

            # Define a function for calculating the integral
            def integral_solution():
                # Use the variables from the page state
                c, d, n, a, b = retrieve_display_variables()
                integral_c = (c / (n + 1)) * (b ** (n + 1) - a ** (n + 1))  # Integral of cx^n over [a, b]
                integral_d = d * (b - a)  # Integral of d over [a, b]
                return integral_c + integral_d

            # Calculate the solution using the defined function
            solution = integral_solution()
            params = problem_display_ending(solution, 'number')

            # Optional preview mode
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)
