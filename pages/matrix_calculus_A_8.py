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
			display_new_line(r'''Given a symmetric matrix B, the derivative of $f(x) = x^T %s x + x^T %s x + v^T x + q$ as''',(v2,v3))
			display_new_line(r'''$$\frac{df}{dx} = %s$$''',(v1))
			display_new_line(r'''what is ❓''')
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			v1 = getInt(0,5,'v1')
			v2 = getRandLetter(sessionID='v2', letter_type='upper_case', ignore_letters=['X'])
			v3 = getRandLetter(sessionID='v3', letter_type='upper_case', ignore_letters=['X', v2])

			L = ['(❓ + ❓^T + %s^T+%s)x + v'%(v3,v3), '(%s + %s^T + ❓^T+%s)x + v'%(v2, v2, v3), '(%s + %s^T + %s^T+❓)x + v'%(v2,v2,v3), '❓(%s + %s^T + %s^T + %s) x + v'%(v2,v2,v3,v3), '(%s + %s^T + %s^T + %s)❓ + v'%(v2,v2,v3,v3), '(%s + %s^T + %s^T + %s)x + ❓'%(v2,v2,v3,v3), '(%s + %s^T + %s^T + %s)x + q + ❓'%(v2,v2,v3,v3)]
			L2 = [v2, v3, v3, '1', 'x', 'v', '0']

			# define key variables and display the problem
			set_page_variables_for_display([L[v1], v2, v3])
			display_problem()

			# define the solution	
			solution = L2[v1]

			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

