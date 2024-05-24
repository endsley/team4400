import streamlit as st
import numpy as np
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()

            [x] = retrieve_display_variables()
            display_new_line(r'''If on average a person needs to have $$%d$$ serious relationships before they end up with the right person, what is
the probability that the first person you date is the right person? Answer as a decimal between 0 and 1 rounded to 4 decimal places.''', x)


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # generate random data
            x = getInt(2, 10)

			# define key variables and display the problem
            set_page_variables_for_display([x])
            display_problem()

			# define the solution	
            # poisson(1 | theta = x) = x^1 * e^-x / 1! = x * e^-x
            solution = round(x * np.exp(-x), 4)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

