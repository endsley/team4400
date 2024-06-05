#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 24 16:41:03 2023

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
			display_new_line(r'''Which of the following is true for regression methods in the case of feature selection?''')
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

			v1 = multiple_choice(['Lasso regression uses subset selection of features',
                         'Ridge regression uses subset selection of features', 
                          
                         'Both Ridge regression and Lasso regression use subset selection of features'], 'v1')

			set_page_variables_for_display([v1])
			display_problem()

			# define the solution	
			solution = v1[0]
			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)
