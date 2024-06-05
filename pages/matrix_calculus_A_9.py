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
			[v1, v2, v3, v4] = retrieve_display_variables()
			display_new_line(r''' Given $$\alpha = \begin{bmatrix} %d \\ %d \\ %d \end{bmatrix}$$, $$x = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}$$ and ''',(v1, v2, v3))
			display_new_line(r''' $$ f(x) = ||x||_1 \quad,\quad \nabla f(\alpha) = \begin{bmatrix} a \\ b \\ c \end{bmatrix} $$ What is then $%s$ ? ''',(v4))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3] = getMultInts(3, -7, 9)
			v4 = getInt(0,2,'v4')
			L = [np.sign(v1), np.sign(v2), np.sign(v3)]
			L2 = ['a', 'b', 'c']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3 , L2[v4]])
			display_problem()

			# define the solution	
			solution = L[v4]

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

