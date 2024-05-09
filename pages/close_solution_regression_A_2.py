#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import time

if __name__ == "__main__":
	n_sec = 8*60

	def display():
		def display_problem():
			display_color_problem_title()
	
			[v1, v2, v3, v4, v5, v6, v7, v8, v9, v10] = retrieve_display_variables()
			display_new_line(r'''Given a linear regression objective of $\min_w \quad \frac{1}{2} \sum_i^n (f_w(x) - y_i)^2$''')
			display_new_line(r'''where the hypothesis function is defined as $f(x) = w_1 x_1 + w_2 x_2$.''')
			display_new_line(r'''Given a data Matrix $X = \begin{bmatrix} %d & %d \\ %d & %d \\ %d & %d \end{bmatrix}$, and label of $y = [%d,%d,%d]^T$, ''',(v1,v2,v3,v4,v5,v6,v7,v8,v9))
			display_new_line(r'''Given the solution as $w = \begin{bmatrix} a \\ b \end{bmatrix}$, what is $%s$ using the closed-form solution? (Use 0 if no solution exists)''',(v10))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4, v5, v6, v7, v8, v9] = getMultInts(9, -2, 2)
			v10 = getInt(0,1,'v10')
			L = ['a','b']

			# display the problem
			set_page_variables_for_display([v1, v2, v3, v4, v5, v6, v7, v8, v9, L[v10]])
			display_problem()

			# define the solution	
			y = np.array([[v7],[v8],[v9]])
			Φ = np.array([[v1, v2], [v3,v4], [v5,v6]])

			try:
				w = np.linalg.inv(Φ.T.dot(Φ)).dot(Φ.T).dot(y)
				solution = w[v10].item()
			except:
				solution = 0

			params = problem_display_ending(solution, 'number')
		return params

	standard_problem_page(n_sec, display)

