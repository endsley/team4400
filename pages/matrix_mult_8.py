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
			[v1, v2, v3,v4, v5] = retrieve_display_variables()
			display_new_line(r''' 
				$$ 
				\begin{bmatrix} %d \\ %d \end{bmatrix}
				\begin{bmatrix} %d & %d \end{bmatrix}
				= 
				\begin{bmatrix} a & b \\ c & d \end{bmatrix}
				$$ 
				''',(v1,v2,v3,v4))
			display_new_line(r'''what is the value of $%s$ ?''',(v5))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3, v4] = getMultInts(4, -2, 2)
			v5 = getInt(0,3,'v5')
			L = ['a','b','c','d']

			# define key variables and display the problem
			set_page_variables_for_display([v1,v2,v3,v4, L[v5]])
			display_problem()

			# define the solution	
			a = np.array([[v1],[v2]])
			b = np.array([[v3,v4]])
			solution = np.reshape(a.dot(b), (1,4))[0][v5]

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

