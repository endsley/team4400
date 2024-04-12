import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 300

    def display():
        def display_problem():
            display_color_problem_title()
            (sample_1, sample_2, sample_3) = retrieve_display_variables()
            display_new_line(
                r''' 
                Given 3 samples $x=\left\{%d, %d, %d \right\}$, what's $E[(x - \mu)^{2}]$? (Round to 1 decimal point)
                ''',
                (sample_1, sample_2, sample_3)
            )

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # get values for matrix and display
            mat_vals = getMultInts(3, -4, 4)
            (sample_1, sample_2, sample_3) = mat_vals
            set_page_variables_for_display([sample_1, sample_2, sample_3])
            display_problem()            
            
            # calculate the estimated solution
            samples = [sample_1, sample_2, sample_3]
            solution = round(np.mean([(sample - np.mean(samples)) ** 2 for sample in samples]), 1)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

