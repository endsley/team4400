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
			[v1, v2, v3,v4] = retrieve_display_variables()
			display_new_line(r'''Given $a = [%d,%d]^T, b = [%d,%d]^T$, what's $a \cdot b $? ''',(v1,v2,v3,v4))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4] = getMultInts(4, -2, 5)

			# define key variables and display the problem
			set_page_variables_for_display([v1,v2,v3,v4])
			display_problem()

			# define the solution	
			a = np.array([v1, v2])
			b = np.array([v3, v4])
			solution = a.dot(b)

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

