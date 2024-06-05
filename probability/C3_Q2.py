#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
import random
from math import isclose
import time
from scipy.integrate import quad

if __name__ == "__main__":
	n_sec = 100

	def display():
		#	Define this function for new problem
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[a, b] = retrieve_display_variables()
			display_new_line(r''' If on average students wait until the last $$ %d $$ days to start studying for an exam, 
			what is the probability that a student starts studying before $$ %d $$ days? Round to the nearest 2 decimal places.''',(a, b))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			a = getInt(1,3)
			b = getInt(3,4)

			# define key variables and display the problem
			set_page_variables_for_display([a, b])
			display_problem()

			integral = quad(lambda x: (1/a)*np.exp((-1/a)*x), 0, b)

			# define the solution
			solution = np.round(1-integral[0], 2)
			params = problem_display_ending(solution, 'number')

			if 'preview' in st.session_state and st.session_state['preview'] == 1:
				st.write("Solution is: " + str(solution))

		return params

	standard_problem_page(n_sec, display)


