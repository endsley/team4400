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
			[v1, v2] = retrieve_display_variables()
			display_new_line(r'''Given the following two distributions''')
			col1, col2 = st.columns([1,1])

			with col1: 
				image = Image.open('./pages/images/continuous_distribution.png')
				st.image(image, caption='Distribution A')
			with col2: 
				image2 = Image.open('./pages/images/discrete_distribution.png')
				st.image(image2, caption='Distribution B')


			display_new_line(r'''Distribution %s is call a ? distribution''',(v1))
			display_multiple_choice(v2)

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1] = getMultInts(1, 0, 1)
			L = ['A','B']
			L2 = ['continuous','discrete']

			if L2[v1] == 'continuous':
				alt = 'discrete'
			else:
				alt = 'continuous'

			v2 = multiple_choice([L2[v1], 
                         alt, 
                         'Normal',
                         'None of the options'], 'v2')



			# define key variables and display the problem
			set_page_variables_for_display([L[v1], v2])
			display_problem()

			# define the solution	
			solution = v2[0]

			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

