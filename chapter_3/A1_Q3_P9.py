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
from scipy.stats import norm 


# In[9]:


if __name__ == "__main__":
    n_sec=8*60


    def display():
        def display_problem():
            display_color_problem_title()

            # Formation of a function of the form coefficient*x^exponent + constant
            [rand_constant, k_mul, sample_pairs] = retrieve_display_variables()
            display_new_line(r''' You are using a uniform distribution between -%d to %d to perform rejection sampling on a Gaussian distribution''', (rand_constant, rand_constant))
            display_new_line(r''' of $(\mu=0,\sigma=1)$. Let the $k$ multiplier be %d. In rejection sampling, you generate 2 values for each possible sample $(v_1, v_2)$,''', (k_mul))
            display_new_line(r''' where $v_1$ is the sample and $v_2$ gives you the acceptance rate. From this, you generated 3 pairs (%.1f, %.1f), (%.1f, %.1f), (%.1f, %.1f).''', (sample_pairs[0][0], sample_pairs[0][1], sample_pairs[1][0], sample_pairs[1][1], sample_pairs[2][0], sample_pairs[2][1]))
            display_new_line(r''' Enter which samples were generated. ''')


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # Generate random variables for function of the form
            solutions = []
            rand_constant = np.random.randint(2, 10)
            k_mul = 2 * rand_constant
            sample_array = np.random.choice(4, 3, replace=False) - 2
            #generate one that passes
            p1_upperbound = norm.pdf(sample_array[0], 0, 1)
            pair1 = [sample_array[0], np.round(np.random.uniform(0.1, p1_upperbound), 1)]
            solutions.append(pair1)
            #generate one that fails
            pair2 = [sample_array[1], np.round(np.random.uniform(norm.pdf(sample_array[1], 0, 1), (2 * norm.pdf(sample_array[1], 0, 1))), 1)]
            #generate one that can be either
            pair3 = [sample_array[2], np.round(np.random.uniform(0.1, (2 * norm.pdf(sample_array[2], 0, 1))), 1)]
            if (pair3[1] > norm.pdf(sample_array[2], 0, 1)):
                solutions.append(pair3)
            sample_pairs = [pair1, pair2, pair3]
            np.random.shuffle(sample_pairs)
            
            
            # display the problem 
            set_page_variables_for_display([rand_constant, k_mul, sample_pairs])
            display_problem()
      
            def samples_solution():
                return solutions

            #solution = integration_estimate(upper_limit, sample1, sample2)
            solution = samples_solution()

            params = problem_display_ending(solution, 'number')

            # if in adding questions mode, display the solution
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)


# In[ ]:




