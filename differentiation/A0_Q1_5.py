import streamlit as st
import numpy as np
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()
            [random_x, x_expon] = retrieve_display_variables()
            display_new_line(r''' What is the derivative value of $f(x) = log_2\left(\frac{1}{x^{%d}}\right) $ when $x = %d $''', (x_expon, random_x))

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            [random_x,x_expon] = getMultInts(2, 1, 4)
            set_page_variables_for_display([random_x,x_expon])
            display_problem()
            def derivative(x):
                return -(np.log2(x)*x_expon)
            solution = derivative(random_x)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

