import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 240

    def display():
        def display_problem():
            display_color_problem_title()
            (sample_1, sample_2, sample_3, exp_val) = retrieve_display_variables()
            display_new_line(
                r''' 
                Given 3 samples $x=\left\{%d, %d, %d \right\}$, what's $E[x - %d]$? (Round to 1 decimal point)
                ''',
                (sample_1, sample_2, sample_3, exp_val)
            )

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # get values for matrix and display
            mat_vals = getMultInts(4, 1, 5)
            (sample_1, sample_2, sample_3, exp_val) = mat_vals
            set_page_variables_for_display([sample_1, sample_2, sample_3, exp_val])
            display_problem()            
            
            # calculate the estimated solution
            samples = [sample_1, sample_2, sample_3]
            solution = round(np.mean([sample - exp_val for sample in samples]), 1)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

