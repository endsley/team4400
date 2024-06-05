import streamlit as st
from utils import *
import sympy as sp
import numpy as np


if __name__ == "__main__":
    n_sec = 50

    def display():
        #    Define this function for new problem
        def display_problem():
            display_color_problem_title()

            #    parts where you change
            random_coefficient = np.random.randint(-10, 10) + 1
            random_index = np.random.randint(1, 4)
            random_x = np.random.randint(-10, 10)
            random_addon = np.random.randint(-100, 100)
            x = sp.symbols('x')
            expression = random_coefficient * x ** random_index + random_addon

            # Display the mathematical expression in LaTeX format
            display_new_line(f"What is the derivative value of ${sp.latex(expression)}$ when $x = {random_x}$?")
            return (random_coefficient, random_index, random_x, random_addon)
        # -------------------------------------------------------------------

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # generate random data
#            random_coefficient = np.random.randint(-10, 10)
#            random_index = np.random.randint(1, 4)
#            random_x = np.random.randint(-10, 10)
#            random_addon = np.random.randint(-100, 100)

            # define key variables and display the problem
            random_coefficient, random_index, random_x, random_addon = display_problem()
            set_page_variables_for_display([random_coefficient, random_index, random_x, random_addon])

            # define the solution
            x = sp.symbols('x')
            expression = random_coefficient * x ** random_index + random_addon
            derivative = sp.diff(expression, x)
            solution = derivative.subs(x, random_x)
            params = problem_display_ending(solution, 'number')
            
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

#def calculate_derivative_at_random_point():
#    # Define the variable and the expression
#    x = sp.symbols('x')
#    expression = 2*x**2 + 1
#
#    # Calculate the derivative
#    derivative = sp.diff(expression, x)
#
#    # Generate a random integer for x
#    random_integer = np.random.randint(-10, 10)
#
#    # Evaluate the derivative at the random integer
#    result = derivative.subs(x, random_integer)
#
#    return result

