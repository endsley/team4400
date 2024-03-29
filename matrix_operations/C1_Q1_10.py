#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import time

if __name__ == "__main__":
	n_sec = 60

	def display():
		#	Define this function for new problem
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[a, b, c, d, e, f, g, h, v] = retrieve_display_variables()
			display_new_line(r''' X =  $$ \begin{bmatrix}
							%d & %d \\%d & %d\end{bmatrix} $$ , Y = $$  \begin{bmatrix}%d & %d \\%d & %d
						\end{bmatrix} $$''',(a, b, c, d, e, f, g, h))
			display_new_line(r'''$$ (X \odot Y) - I = \begin{bmatrix} a & b \\ c & d\end{bmatrix} $$, What is $$%s$$ ?''',(v))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[a, b, c, d, e, f, g, h] = getMultInts(8, -4, 4)
			v = getInt(0,4,'v')
			L = ['a', 'b', 'c', 'd']

			# define key variables and display the problem
			set_page_variables_for_display([a, b, c, d, e, f, g, h, L[v]])
			display_problem()

			# define the solution
			X = np.array([[a, b],
						 [c, d]])
			Y = np.array([[e, f],
						 [g, h]])
			I = np.array([[1, 0],
						 [0, 1]])
			solution = ((X*Y) - I)[v//2, v%2].item()
			params = problem_display_ending(solution, 'number')

			if 'preview' in st.session_state and st.session_state['preview'] == 1:
				st.write("Solution is: " + str(solution))

		return params

	standard_problem_page(n_sec, display)

