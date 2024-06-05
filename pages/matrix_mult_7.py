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
			[v1, v2, v3,v4] = retrieve_display_variables()
			display_new_line(r'''Given the following Python code, what is z (write 0 if it triggers an error)?''')
			display_new_line("""
			```python
			import numpy as np	
			
			x = np.array([%d, %d])
			y = np.array([%d, %d])
			z = x.dot(y)
			```
			""",(v1,v2,v3,v4))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1 ,v2 ,v3 ,v4] = getMultInts(4, -3, 3)

			# define key variables and display the problem
			set_page_variables_for_display([v1,v2,v3,v4])
			display_problem()

			# define the solution	
			a = np.array([v1,v2])
			b = np.array([v3,v4])
			solution = a.dot(b)

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

