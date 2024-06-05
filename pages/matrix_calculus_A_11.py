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
			display_new_line(r'''Given $f(x) = ||x||_2$,  $v = \begin{bmatrix} %d \\ %d \\ %d \end{bmatrix}$ and ''',(v1, v2, v3))
			display_new_line(r'''$$ \nabla f(x) = %s$$ ''',(v4))
			display_new_line(r'''what is ❓''')
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3] = getMultInts(3, -1, 2)
			v4 = getInt(0,2,'v4')
			L = [r'\frac{❓}{||x||_2}',r'\frac{x}{||❓||_2}', r'\frac{x}{||x||_❓}', r'\frac{1}{||x||_2} \begin{bmatrix} ❓ \\ b \\ c \end{bmatrix}', r'\frac{1}{||x||_2} \begin{bmatrix} a \\ ❓ \\ c \end{bmatrix}', r'\frac{1}{||x||_2} \begin{bmatrix} a \\ b \\ ❓ \end{bmatrix}']
			L2 = ['x','x', '2', str(v1), str(v2), str(v3)]

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, L[v4]])
			display_problem()

			# define the solution	
			solution = L2[v4]

			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

