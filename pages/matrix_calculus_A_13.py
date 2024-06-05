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
			[v1, v2, v3, v4, v5] = retrieve_display_variables()
			display_new_line(r'''Given $f(x) = ||x||_2$,  $v = \begin{bmatrix} %d \\ %d\end{bmatrix}$ and ''',(v1, v2))
			display_new_line(r'''$$ \nabla f^T(v) \nabla f(v) = \frac{%s}{%s}$$ ''',(v3, v4))
			display_new_line(r'''what is %s''',(v5))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			v1 = getInt(0,3,'v1')
			v2 = getInt(1,4,'v2')

			v3 = 'a' #getRandEmoji(sessionID='v3')
			v4 = 'b' #getRandEmoji(sessionID='v4')
			v5 = getInt(0,1,'v5')
			L = [v3, v4]

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, v4, L[v5]])
			display_problem()

			# define the solution	
			x = np.array([[v1],[v2]])
			solution = (x.T.dot(x)).item()

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

