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
			[v1,v2,v3,v4,v5,v6,v7,v8,v9] = retrieve_display_variables()
			display_new_line(r'''Given $%s = \begin{bmatrix} %d \\ %d \end{bmatrix}$ ''',(v6, v1,v2))
			display_new_line(r'''Given $%s = \begin{bmatrix} %d \\ %d \end{bmatrix}$ ''',(v8, v3,v4))
			display_new_line(r'''The triangle inequality for norms states that $||%s + %s||_%s$ will always be less than what value? ''',(v6, v8, v9))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4] = getMultInts(4, -3, 3)

			v5 = getInt(0,1,'v5')
			v6 = getRandEmoji('v6')
			L = ['||%s||_1'%v6, '||%s||_{\infty}'%v6]

			v7 = getInt(0,1,'v7')
			v8 = getRandEmoji('v8', ignor_list=[v6])
			L2 = ['||%s||_1'%v8, '||%s||_{\infty}'%v8]

			v9 = getInt(0,1,'v9')
			L3 = ['1', '{\infty}']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, v4, L[v5], v6, L2[v5], v8, L3[v5]])
			display_problem()

			# define the solution	
			a = np.array([v1, v2])
			b = np.array([v3, v4])

			A = vector_to_norm(a, L[v5].replace(v6, 'x'))
			B = vector_to_norm(b, L2[v5].replace(v8, 'x'))
			solution = A + B

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

