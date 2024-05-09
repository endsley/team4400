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
			[v1, v2, v3, v4, v5, v6, v7] = retrieve_display_variables()
			display_new_line(r''' $$\begin{bmatrix} %d \\ %d \end{bmatrix} + \begin{bmatrix} %d \\ %d \end{bmatrix} + \begin{bmatrix} %d \\ %d \end{bmatrix}= \begin{bmatrix} a \\ b \end{bmatrix}$$ ''',(v1, v2, v3, v4, v5, v6))
			display_new_line(r''' What is $$%s$$ ?''',(v7))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4, v5, v6] = getMultInts(6, -8, 8)
			v7 = getInt(0,1,'v7')
			L = ['a', 'b']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3 , v4, v5, v6, L[v7]])
			display_problem()

			# define the solution	
			a = np.array([v1, v2])
			b = np.array([v3, v4])
			c = np.array([v5, v6])
			solution = (a + b + c)[v7].item()
			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

