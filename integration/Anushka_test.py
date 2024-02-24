import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()
            [random_addon, random_coefficient, power, random_lower, random_upper] = retrieve_display_variables()
            display_new_line(r''' What is the integral value of $\int^{%d}_{%d} %dx^%d + %d dx$''', 
                             (random_upper, random_lower, random_coefficient, power, random_addon))


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            [random_addon, random_coefficient, power] = getMultInts(3, 2, 5)
            [random_lower] = getMultInts(1, 0, 5)
            [random_upper] = getMultInts(1, random_lower + 1, 10)
            set_page_variables_for_display([random_addon, random_coefficient, power, random_lower, random_upper])
            display_problem()
            def anti_derivative(x):
                return random_coefficient * (1 / (power + 1)) * x**(random_coefficient + 1) + random_coefficient
            def solve_anti_deriv():
                return anti_derivative(random_upper) - anti_derivative(random_lower)
            solution = solve_anti_deriv()
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

