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
			[v1, v2, v3, v4, v5, v6, v7, v8, v9] = retrieve_display_variables()
			display_new_line(r'''Given ''')
			display_new_line(r'''$$x_1 = \begin{bmatrix} %d \\ %d \end{bmatrix}, \quad x_2 = \begin{bmatrix} %d \\ %d \end{bmatrix}, \quad p = \begin{bmatrix} %d \\ %d \end{bmatrix} $$''',(v1,v2,v3,v4,v5,v6))
			display_new_line(r'''$$y_1 = %d, y_2 = %d $$''',(v7,v8))
			display_new_line(r'''and''')
			display_new_line(r'''$$f(w) = \frac{1}{2} \sum_{i=1}^2 (w^T x_i - y_i)^2$$''')
			display_new_line(r'''what is the %s of the vector $\nabla f(p)$ ?''',(v9))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4, v5, v6] = getMultInts(6, -1, 2)
			v7 = getInt(0,1,'v7')
			v8 = getInt(0,1,'v8')

			v9 = getInt(0,4,'v9')
			L = ['maximum','minimum', 'total sum', 'L1 norm', 'infinity norm']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, v4, v5, v6, v7, v8, L[v9]])
			display_problem()

			# define the solution	
			x1 = np.array([[v1],[v2]])	
			x2 = np.array([[v3],[v4]])	
			p = np.array([[v5],[v6]])	
			r = (p.T.dot(x1) - v7)*x1 + (p.T.dot(x2) - v8)*x2 
			solution = vector_to_norm(r, L[v9])

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

