import streamlit as st
from utils import *
import numpy as np
from math import isclose
import sympy as sp
import numpy as np
import time
import math

if __name__ == "__main__":
    n_sec=8*60


    def display():
        def display_problem():
            display_color_problem_title()

            # Formation of a function of the form coefficient*x^exponent + constant
            [coefficient, x_exponent, x_value ] = retrieve_display_variables()
            display_new_line(r'''What is the derivative value of $f(x) = %de^{x^{%d}}$ when $x = %d$. Provide solution up to third decimal place. ''', (coefficient, x_exponent, x_value))



        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # Generate random variables for function of the form
            [coefficient, x_exponent, x_value] = getMultInts(3, 1, 2)

            # display the problem 
            set_page_variables_for_display([coefficient, x_exponent, x_value])
            display_problem()

            def derivative(coefficient, x_exponent, x_value):
                solution = coefficient * (math.e ** (x_value)** x_exponent) * (x_exponent * (x_value)**(x_exponent - 1))
                return solution

            #solution = round(derivative(coefficient, x_exponent, x_value),3)
            solution ="{:.3f}".format(derivative(coefficient, x_exponent, x_value))

            params = problem_display_ending(solution, 'number')

            # if in adding questions mode, display the solution
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)


