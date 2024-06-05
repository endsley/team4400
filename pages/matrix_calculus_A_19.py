#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import time

if __name__ == "__main__":
	n_sec = 60

	def display():
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[v1, v2, v3, v4, v5, v6, v7] = retrieve_display_variables()

			display_new_line(r'''Given $x = [%d, %d]^T$ and ''', (v1,v2))
			display_new_line(r'''$$A = \begin{bmatrix} %d & %d \\ %d & %d \end{bmatrix}$$''',(v3,v4,v5,v6))
			display_new_line(r'''The derivative of''')
			display_new_line(r'''$$f(x) = e^{-x^T A x}$$''')
			display_new_line(r'''is''')
			display_new_line(r'''$f'(x) = f(x) \begin{bmatrix} a \\ b \end{bmatrix} $''')
			display_new_line(r'''what is $%s$''',v7)
		# -------------------------------------------------------------------
		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4, v5, v6] = getMultInts(6, -2, 2)
			v7 = getInt(0,1,'v7')
			L = ['a','b']

			# display the problem
			set_page_variables_for_display([v1, v2, v3, v4, v5, v6, L[v7]])
			display_problem()

			# define the solution	
			x = np.array([[v1],[v2]])
			A = np.array([[v3, v4],[v5, v6]])
			v = -(A.T + A).dot(x)
			solution = v[v7][0]

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

