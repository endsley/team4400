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
			[v1, v2, v3, v4, v5, v6, v7] = retrieve_display_variables()
			display_new_line(r'''Given $w = [%d, %d, %d]^T$ and $x = [%d, %d, %d]^T$''',(v1,v2,v3,v4,v5,v6))
			display_new_line(r'''$$f(w) = ReLU(w^T x).$$''')
			display_new_line(r'''It's derivative is''')
			display_new_line(r'''$f'(w) = [a, b, c]$''')
			display_new_line(r'''what is $%s$''',(v7))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4, v5, v6] = getMultInts(6, -2, 2)
			v7 = getInt(0,2,'v7')
			L = ['a','b','c']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, v4, v5, v6, L[v7]])
			display_problem()

			# define the solution	
			w = np.array([[v1],[v2],[v3]])
			x = np.array([[v4],[v5],[v6]])
			if w.T.dot(x) < 0: solution = 0
			else: solution = x[v7][0]

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

