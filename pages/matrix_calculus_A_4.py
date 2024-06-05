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
			[v1, v2, v3, v4, v5] = retrieve_display_variables()
			display_new_line(r''' Given $v_1  = \begin{bmatrix} %d \\ %d \end{bmatrix}$ and $v_2  = \begin{bmatrix} %d \\ %d \end{bmatrix}$ and ''',(v1, v2, v3, v4))
			display_new_line(r'''$$ f(x) = \sum_{i=1}^2 v_i^T x + u $$ ''')
			display_new_line(r'''where''')
			display_new_line(r''' $$\frac{df}{dx} = \begin{bmatrix} a \\ b \end{bmatrix}$$, ''')
			display_new_line(r''' what is the value of $%s$?''',(v5))


		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4] = getMultInts(4, -4, 5)
			v5 = getInt(0,1,'v5')
			L = ['a','b']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3,v4, L[v5]])
			display_problem()

			# define the solution	
			A = np.array([v1, v2])
			B = np.array([v3, v4])
			C = A + B
			solution = C[v5]

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

