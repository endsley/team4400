#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import pandas as pd
import time

if __name__ == "__main__":
	n_sec = 50

	def display():
		#	Define this function for new problem
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[v1] = retrieve_display_variables()
			display_new_line(r'''Given the following table''')

			data = {"events": ['y=0', 'y=1', 'y=2'], 'x=0': [0, 0.5, 0.1], 'x=1': [0.2, 0.1, 0.1]}
			chart_data = pd.DataFrame( data )
			chart_data.set_index('events', inplace=True)

			st.write(chart_data)
			display_new_line(r'''what is %s?''',(v1))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1] = getMultInts(1, 0, 9)
			L = ['p(x=1,y=1)','p(x=0, y=2)','P{x=0 and y=0}', 'p(x=0)', 'p(x=1)', 'p(y=0)', 'p(y=1)', 'p(y=2)', 'P{x=0 U y=1}', 'P{x=1 U y=1}']

			# define key variables and display the problem
			set_page_variables_for_display([L[v1]])
			display_problem()

			# define the solution	
			if v1 == 0: solution = 0.1
			if v1 == 1: solution = 0.1
			if v1 == 2: solution = 0
			if v1 == 3: solution = 0.6
			if v1 == 4: solution = 0.4
			if v1 == 5: solution = 0.2
			if v1 == 6: solution = 0.6
			if v1 == 7: solution = 0.2
			if v1 == 8: solution = 0.7
			if v1 == 9: solution = 0.9

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

