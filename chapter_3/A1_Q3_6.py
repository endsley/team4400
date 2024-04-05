import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 600

    def display():
        def display_problem():
            display_color_problem_title()
            rand_nums = retrieve_display_variables()
            display_new_line(
                r''' 
                Given a Gaussian distribution with $\mu = %d$ and $\sigma = 1$, we wish to find the $E[%dx^{2}+%d]$ by using sampling to solve the integral:
                ''',
                tuple(rand_nums[0])
            )
            display_new_line(
                r''' 
                $\int (%dx^2+%d)\frac{1}{\sigma \sqrt{2\pi}}e^{-\frac{(x-\mu )^{2}}{2\sigma ^{2}}}$
                ''',
                tuple(rand_nums[1])
            )

            display_new_line(
                r''' 
                If you only generated 2 samples of the values %d and %d, what is the estimated solution to the integral using these 2 samples?  (Round to 1 decimal point)
                ''',
                tuple(rand_nums[2])
            )

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # get values for matrix and display
            mat_vals = getMultInts(5, 2, 6)
            (gaussian_mu, exp_coeff, exp_const, sample_1, sample_2) = mat_vals
            set_page_variables_for_display([[gaussian_mu, exp_coeff, exp_const], [exp_coeff, exp_const], [sample_1, sample_2]])
            display_problem()
            
            # def sample_exp function
            def sample_exp(sample, exp_coeff=exp_coeff, exp_const=exp_const):
                return (exp_coeff * (sample ** 2) + exp_const) 
            
            # calculate the estimated solution
            solution = round((sample_exp(sample_1) + sample_exp(sample_2)) / 2, 1)

            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

