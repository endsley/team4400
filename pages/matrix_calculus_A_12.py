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
			display_new_line(r'''$$ \nabla f(v) = %s$$ ''',(v4))
			display_new_line(r'''what is ❓''')
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2] = getMultInts(2, -4, 4)
			v3 = getInt(1,4,'v3')
			v4 = getInt(0,3,'v4')

			L = [r'\frac{1}{\sqrt{❓}} \begin{bmatrix} a \\ b \\ c \end{bmatrix}', r'\frac{1}{||x||_2} \begin{bmatrix} ❓ \\ b \\ c \end{bmatrix}', r'\frac{1}{||x||_2} \begin{bmatrix} a \\ ❓ \\ c \end{bmatrix}', r'\frac{1}{||x||_2} \begin{bmatrix} a \\ b \\ ❓ \end{bmatrix}']
			L2 = [v1*v1 + v2*v2 + v3*v3, v1, v2, v3]

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, L[v4]])
			display_problem()

			# define the solution	
			solution = L2[v4]

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

