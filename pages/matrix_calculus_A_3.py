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
			[v1, v2, v3] = retrieve_display_variables()
			display_new_line(r''' Given $%s \in \mathbb{R}^%s, %s \in \mathbb{R}$ $$f(x) = %s^T x + %s$$''',(v1, v3, v2, v1, v2))
			display_new_line(r''' What is the dimension of $ \frac{df}{dx} ?  $ ''')

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			v1 = getRandLetter('v1', ignore_letters=['x', 'l'])
			v2 = getRandLetter('v2', ignore_letters=['x',v1, 'l'])
			v3 = getRandLetter('v3', ignore_letters=['x',v1, v2, 'l'])

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3])
			display_problem()

			# define the solution	
			solution = v3

			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

