#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 17:04:57 2023

@author: tingtingzhao
"""

#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import pandas as pd
from PIL import Image
import time

if __name__ == "__main__":
	n_sec = 50

	def display():
		#	Define this function for new problem
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[v1] = retrieve_display_variables()
			display_new_line(r'''Consider the following two regression models. Model1: $y_t=\beta_1+\beta_2 x_{2t}+\mu_t$. Model2: $y_t=\alpha_1+\alpha_2 x_{2t}+\alpha_3 x_{3t}+\mu_t$.Where $x_{2t}$ is the exact same feature in two models with same observations in the dataset. Which of the following statements are true? (i)Model 2 must have an R2 at least as high as that of model 1; (ii) Model 2 must have an adjusted R2 at least as high as that of model 1; (iii) Models 1 and 2 would have identical values of R2 if the estimated coefficient on $\alpha_3$ is zero; (iv) Models 1 and 2 would have identical values of adjusted R2 if the estimated coefficient on $\alpha_3$ is zero''')
			display_multiple_choice(v1)

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			#	randomize multiple choice
			#v1 = multiple_choice([	'joint distribution', 	# first one is always the answer
			#						'multi-distribution',	# the code will automatically randomize for you
			#						'poly-distribution' ], 'v1')	# Very import to include the session id for variable used

			v1 = multiple_choice(['(i) and (iii) only',
                         '(ii) and (iv) only', 
                          
                         '(i), (ii), (iii) only',
                         '(i), (ii), (iii), (iv) only'], 'v1')

			set_page_variables_for_display([v1])
			display_problem()

			# define the solution	
			solution = v1[0]
			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)
