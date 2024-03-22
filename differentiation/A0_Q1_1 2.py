import streamlit as st
from utils import *
import numpy as np
from math import isclose
import sympy as sp
import numpy as np
import time

if __name__ == "__main__":
    n_sec=8*60


    def display():
        def display_problem():
            display_color_problem_title()

            # Formation of a function of the form coefficient*x^exponent + constant
            [coefficient, exponent, constant, x_value ] = retrieve_display_variables()
            display_new_line(r''' What is the derivative value of $f(x) = %d x^{%d} + %d$ when $x = %d $''' , (coefficient, exponent, constant, x_value))



        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # Generate random variables for function of the form
            [coefficient, exponent, constant, x_value] = getMultInts(4, 2, 6)

            # display the problem 
            set_page_variables_for_display([coefficient, exponent, constant, x_value])
            display_problem()

            def derivative(coefficient, exponent, constant, x_value):
                new_exponent = exponent - 1
                solution = coefficient * exponent * ((x_value) ** new_exponent) 
                return solution

            solution = derivative(coefficient, exponent, constant, x_value)

            params = problem_display_ending(solution, 'number')

            # if in adding questions mode, display the solution
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)










        
        