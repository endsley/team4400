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
			[v1, v2] = retrieve_display_variables()
			display_new_line(r'''In the following Python code, what is the value of %s?).''',(v2))
			display_new_line("""
			```python
			import numpy as np	
			
			x = np.array([3,4])
			%s = np.linalg.%s
			```
			""",(v2,v1))
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			v1 = getInt(0,7,'v1')
			v2 = getRandEmoji('v2')
			L = ['norm(x,ord=1)', 'norm(x,ord=2)', 'norm(x,ord=np.inf)', 'norm(x,ord=1)', 'norm(x,ord=2)', 'norm(x,ord=np.inf)', 'norm(x,ord=np.inf)', 'norm(x,ord=np.inf)']
			L2 = ['7', '5', '4', '7', '5', '4', '4', '4']

			# define key variables and display the problem
			set_page_variables_for_display([L[v1], v2])
			display_problem()

			# define the solution	
			solution = L2[v1]

			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

