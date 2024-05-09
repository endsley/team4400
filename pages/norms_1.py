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
			[v1, v2, v3] = retrieve_display_variables()
			display_new_line(r'''What is the %s of the vector''',(v3))
			display_new_line(r''' $$ \begin{bmatrix} %d \\ %d \end{bmatrix} = \text{?} $$ ''',(v1, v2))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2] = getMultInts(2, -2, 2)
			v3 = getInt(0,7,'v3')
			L = ['L1 norm', 'L2 norm squared', 'infinity norm', 'Manhattan norm', 'Euclidean norm squared', 'maximum norm', 'uniform norm', 'supremum norm']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, L[v3]])
			display_problem()

			# define the solution	
			a = np.array([v1, v2])
			solution = vector_to_norm(a, L[v3])

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

