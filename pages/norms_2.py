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
			display_new_line(r'''Given $%s = \begin{bmatrix} %d \\ %d \end{bmatrix}$ ''',(v4, v1,v2))
			display_new_line(r'''what is $%s$ ? ''',(v3))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2] = getMultInts(2, -3, 3)
			v3 = getInt(0,2,'v3')
			v4 = getRandEmoji('v4')
			L = ['||%s||_1'%v4, '||%s||_2^2'%v4, '||%s||_{\infty}'%v4]

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, L[v3], v4])
			display_problem()

			# define the solution	
			a = np.array([v1, v2])
			solution = vector_to_norm(a, L[v3].replace(v4, 'x'))

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

