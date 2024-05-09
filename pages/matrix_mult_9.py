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
			display_new_line(r''' Given matrices $A \in \mathbb{R}^{%s \times %s}$, $B \in \mathbb{R}^{%s \times %s}$, and $C \in \mathbb{R}^{a \times b}$''' ,(v1,v2,v2,v3))
			display_new_line(r'''And given $C = AB$''')
			display_new_line(r'''what is $%s$ ?''',(v4))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			v1 = getRandLetter('v1')
			v2 = getRandLetter('v2', ignore_letters=[v1, 'a', 'b'])
			v3 = getRandLetter('v3', ignore_letters=[v1, v2, 'a', 'b'])

			v4 = getInt(0,1,'v4')
			L = ['a', 'b']
			L2 = [v1, v3]

			# define key variables and display the problem
			set_page_variables_for_display([v1,v2,v3,L[v4]])
			display_problem()

			# define the solution	
			solution = L2[v4]

			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

