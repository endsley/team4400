import streamlit as st
import numpy as np
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()
            [random_x, x_expon,rand_const] = retrieve_display_variables()
            display_new_line(r''' What is the derivative value of $f(x) = log((x-%d)^{%d}) $ when $x = %d $''', (rand_const,x_expon, random_x))


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            [random_x,x_expon,rand_const] = getMultInts(3, 1, 4)
            if (random_x<rand_const):
                temp = random_x
                random_x = rand_const
                rand_const = temp
            elif (random_x==rand_const):
                random_x = rand_const+4
            set_page_variables_for_display([random_x,x_expon,rand_const])
            display_problem()
            def derivative(x):
                return (np.log2(x-rand_const)*x_expon)
            solution = derivative(random_x)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

