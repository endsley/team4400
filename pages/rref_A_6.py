#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import time

if __name__ == "__main__":
	n_sec = 50

	def display():
		#	Define this function for new problem
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[original_matrix, value, final_rref] = retrieve_display_variables()
			display_new_line(r'''Given the matrix''')
			display_new_line(original_matrix)
			display_new_line(r'''Is the value %s within the RREF matrix? (input 0 for no and 1 for yes)'''%value)
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()

			[original_matrix, value, final_rref] = retrieve_display_variables()
			additional_display = r'''The final RREF matrix is '''  + final_rref
			params = display_solutions(additional_display)
		else:
			# generate random data

			[in_or_not, original_matrix, final_rref, value] = generate_random_rref(5, 2, sessionID='v1')
			# define key variables and display the problem
			set_page_variables_for_display([original_matrix, value, final_rref])
			display_problem()

			# define the solution	
			solution = in_or_not

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

