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
			[v1, v2, v3, v4, v5, v6, v7, v8] = retrieve_display_variables()
			display_new_line(r''' Given $A  = \begin{bmatrix} %d & %d \\ %d & %d \end{bmatrix}$, $v  = \begin{bmatrix} %d \\%d \end{bmatrix}$ and ''',(v1, v2, v3, v4, v5, v6))
			display_new_line(r'''$$ f(x) = %s + x^T x$$.''',(v8))
			display_new_line(r'''What is the %s value of the vector $\frac{df}{dx}(v)$ ? ''',(v7)) 
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4] = getMultInts(4, -2, 3)
			v5 = getInt(0,2,'v5')
			v6 = getInt(0,2,'v6')

			v7 = getInt(0,4,'v7')
			L = ['maximum','minimum', 'total sum', 'L1 norm', 'infinity norm']

			v8 = getInt(0,4,'v8')
			L2 = ['Tr(A x x^T)','Tr(x x^T A)', 'Tr(A^T x x^T) ', 'Tr(x x^T A^T)', 'Tr(x^T A x)']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3,v4, v5, v6, L[v7], L2[v8]])
			display_problem()

			# define the solution	
			A = np.array([[v1, v2],[v3,v4]])
			v = np.array([[v5],[v6]])
			r = (A + A.T).dot(v) + 2*np.eye(2).dot(v)
			solution = vector_to_norm(r, L[v7])

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

