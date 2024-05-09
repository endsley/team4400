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

			#	write out the problem statement
			[v1, v2, v3, v4] = retrieve_display_variables()
			display_new_line(r'''What is the %s of the vector''',(v4))
			display_new_line(r''' $$ \begin{bmatrix} %d \\ %d \\ %d \end{bmatrix} $$ ''',(v1, v2, v3))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3] = getMultInts(3, -2, 2)
			v4 = getInt(0,7,'v4')
			L = ['L1 norm', 'L2 norm squared', 'infinity norm', 'Manhattan norm', 'Euclidean norm squared', 'maximum norm', 'uniform norm', 'supremum norm']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, L[v4]])
			display_problem()

			# define the solution	
			a = np.array([v1, v2, v3])
			solution = vector_to_norm(a, L[v4])

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

