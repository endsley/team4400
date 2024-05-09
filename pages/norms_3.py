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

			#	write out the problem statement
			[v1] = retrieve_display_variables()
			display_new_line(r'''Given $x \in \mathbb{R}^d$, which letter is wrong with this definition of a p-norm (none if nothin)?''')
			display_new_line(r'''$$%s$$''',(v1))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			v1 = getInt(0,5,'v1')
			L = [r'||x||_p = (\sum_i^d |x_i|^p)^{1/p}']
			L.append(r'||x||_p = (\sum_i^d |x_i|^p)^{1/q}')
			L.append(r'||x||_p = (\sum_i^d |p_i|^p)^{1/p}')
			L.append(r'||x||_p = (\sum_i^n |x_i|^p)^{1/p}')
			L.append(r'||x||_r = (\sum_i^d |x_i|^p)^{1/p}')
			L.append(r'||x||_p = (\sum_i^d |x_i|^t)^{1/p}')
			L2 = ['none', 'q', 'p', 'n', 'r','t']

			# define key variables and display the problem
			set_page_variables_for_display([L[v1]])
			display_problem()

			# define the solution	
			solution = L2[v1]

			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

