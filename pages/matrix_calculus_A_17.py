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
			[v1] = retrieve_display_variables()
			display_new_line(r'''Given the function ''')
			display_new_line(r'''$$f(w) = ReLU(w^T x).$$''')
			display_new_line(r'''It's derivative is''')
			display_new_line(r'''%s''',(v1))
			display_new_line(r'''what is ❓''')
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			v1 = getInt(0,3,'v1')
			L = [    r"$$\nabla f(w) =  ❓1_{w^T x > 0}$$"]
			L.append(r"$$\nabla f(w) =  x 1_{❓^T x > 0}$$")
			L.append(r"$$\nabla f(w) =  x 1_{w^T ❓ > 0}$$")
			L.append(r"$$\nabla f(w) =  x 1_{w^T x > ❓}$$")

			L2 = ['x', 'w', 'x', '0']

			# define key variables and display the problem
			set_page_variables_for_display([L[v1]])
			display_problem()

			# define the solution	
			solution = L2[v1]
			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

