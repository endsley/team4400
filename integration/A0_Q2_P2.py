from utils import *
import math
import numpy as np


# This is the code for assignment 0, question 2, part 2. The question
# asks to find the integral from 0 to 1 of e^x. This code randomizes the upper bound of the integral,
# and asks the student to solve the integral from 0 to b of e^x, where b is randomly generated at runtime.

if __name__ == "__main__":
    n_sec = 600
    def display():
        def display_problem():
            display_color_problem_title()
            [random_b] = retrieve_display_variables()
            display_new_line(r'''Solve the following integral. Round your answer to two decimal places:''')
            display_new_line(r'''$\int_{0}^{%d}e^xdx$''', (random_b))

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            [random_b] = getMultInts(1, 1, 5)
            set_page_variables_for_display([random_b])
            display_problem()

            def integrate(x):
                return math.exp(x)

            solution = integrate(random_b) - integrate(0)
            rounded_solution = np.round(solution, decimals=2)
            params = problem_display_ending(rounded_solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(rounded_solution))

        return params

    standard_problem_page(n_sec, display)
