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

			[v1, v2, v3, v4, v5] = retrieve_display_variables()
			display_new_line(r'''Given a linear regression objective of $\min_w \quad \frac{1}{2} \sum_i^n (w^\top \phi(x_i) - y_i)^2$''')
			display_new_line(r'''where the hypothesis function is defined as $f(x) = w_1 x + w_2$.''')
			display_new_line(r'''Given a 1 dimensional data of $x = [0,1,2,3]^T$, and label of $y = [%d,%d,%d,%d]^T$, ''',(v1,v2,v3,v4))
			display_new_line(r'''Given the solution as $w = \begin{bmatrix} a \\ b \end{bmatrix}$, what is $%s$ using the closed-form solution?''',(v5))

		# -------------------------------------------------------------------
		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4] = getMultInts(4, -1, 1)
			v5 = getInt(0,1,'v5')
			L = ['a','b']

			# display the problem
			set_page_variables_for_display([v1, v2, v3, v4, L[v5]])
			display_problem()

			# define the solution	
			x = np.array([0,1,2,3])
			y = np.array([[v1],[v2],[v3],[v4]])
			Φ = np.array([x, np.ones(len(x))]).T

			w = np.linalg.inv(Φ.T.dot(Φ)).dot(Φ.T).dot(y)
			solution = w[v5].item()

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

