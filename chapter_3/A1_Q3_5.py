#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
from utils import *
import numpy as np
from math import isclose
import sympy as sp
import numpy as np
import time


# In[9]:


if __name__ == "__main__":
    n_sec=8*60


    def display():
        def display_problem():
            display_color_problem_title()

            # Formation of a function of the form coefficient*x^exponent + constant
            [upper_limit, sample1, sample2, rand_constant] = retrieve_display_variables()
            display_new_line(r'''We want to use sampling from a uniform distribution to solve the following integral.''')
            display_new_line(r'''$\int_{0}^{%d} x + %d dx$''', (upper_limit, rand_constant))
            display_new_line(r'''If you only generated 2 samples of the values %.1f and %.1f, what is the estimate solution to the integral using these 2 samples? ''', (sample1, sample2))



        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # Generate random variables for function of the form
            upper_limit = np.random.randint(0, 10)
            sample1 = round(np.random.uniform(0, upper_limit), 1)
            sample2 = round(np.random.uniform(0, upper_limit), 1)
            while (sample2 == sample1):
                sample2 = round(np.random.uniform(0, upper_limit), 1)
            rand_constant = np.random.randint(0, 10)
            

            # display the problem 
            set_page_variables_for_display([upper_limit, sample1, sample2, rand_constant])
            display_problem()
            
            def f(x, rand_constant):
                return x + rand_constant
            
            def integration_estimate(upper_limit, sample1, sample2, rand_constant):
                solution = f(sample1, rand_constant) + f(sample2, rand_constant)
                solution = round(upper_limit/2 * solution, 3)
                return solution

            #solution = integration_estimate(upper_limit, sample1, sample2)
            solution = integration_estimate(upper_limit, sample1, sample2, rand_constant)

            params = problem_display_ending(solution, 'number')

            # if in adding questions mode, display the solution
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)


# In[13]:





# In[ ]:




