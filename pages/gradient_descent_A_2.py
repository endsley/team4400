#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import time

if __name__ == "__main__":
	n_sec = 13*60
	def display():
		#	Define this function for new problem
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[v1, v2, v3, v4, v5, v6, v7, v8] = retrieve_display_variables()
			display_new_line(r'''Given a linear regression objective of $\min_w \quad \frac{1}{2} \sum_i^n (w^\top \phi(x_i) - y_i)^2$''')
			display_new_line(r'''where the feature map is defined as $\phi(x) = \begin{bmatrix} x & 1 \end{bmatrix}^\top$.''')
			display_new_line(r'''Given a 1 dimensional data of $x = [0,1,2,3]^T$, and label of $y = [%d,%d,%d,%d]^T$, ''',(v1,v2,v3,v4))
			display_new_line(r'''$w_0 = [%d, %d]^T$ and with a step size of $\eta=%d$''',(v5,v6, v7))
			display_new_line(r'''Given $w_1 = \begin{bmatrix} a \\ b \end{bmatrix}$, what is $%s$ after 2 step of Gradient Descent?''',(v8))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4, v5, v6] = getMultInts(6, 0, 1)
			[v7] = getMultInts(1, 1, 2)
			v8 = getInt(0,1,'v8')
			L = ['a','b']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, v4, v5, v6, v7, L[v8]])
			display_problem()

			# define the solution	
			w = np.array([[v5],[v6]])
			x = np.array([0,1,2,3])
			y = np.array([[v1],[v2],[v3],[v4]])
			α = v7
			Φ = np.array([x, np.ones(len(x))]).T

			ᐁf = Φ.T.dot(Φ.dot(w) - y)
			w = w - α*ᐁf
			ᐁf = Φ.T.dot(Φ.dot(w) - y)
			w = w - α*ᐁf

			solution = w[v8].item()
			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

