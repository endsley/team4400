import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()
            [random_x, random_addon, random_coefficient, power] = retrieve_display_variables()
            display_new_line(r''' What is the derivative value of $f(x) = (%d x + %d)^%d$ when $x = %d $''', (random_coefficient, random_addon, power, random_x))


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            [random_x, random_addon, random_coefficient, power] = getMultInts(4, 2, 5)
            set_page_variables_for_display([random_x, random_addon, random_coefficient, power])
            display_problem()
            def derivative(x):
                return power * (((random_coefficient * x ) + random_addon) ** (power - 1)) * random_coefficient
            solution = derivative(random_x)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

