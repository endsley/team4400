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
			[v1, v2, v3, v5, v6] = retrieve_display_variables()
			display_new_line(r'''Given the following %s''',(v6))
			data = {"event": ['a', 'b', 'c'], 'occurence': [float(v1), float(v2), float(v3)]}
			chart_data = pd.DataFrame( data )

			if v6 == 'histogram':
				chart_data.set_index('event', inplace=True)
				st.bar_chart(chart_data)
			else:
				st.write(chart_data)

			display_new_line(r'''what is %s?''',(v5))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1, v2, v3] = getMultInts(3, 0, 5)
			v4 = getInt(0,2,'v4')
			L = ['a','b','c']
			v5 = getInt(0,2,'v5')
			L2 = ['the probability of %s'%(L[v4]), 'p(%s)'%L[v4], 'P\{X = %s\}'%L[v4] ]
			v6 = getInt(0,1,'v6')
			L3 = ['histogram', 'table']

			# define key variables and display the problem
			set_page_variables_for_display([v1, v2, v3, L2[v5], L3[v6]])
			display_problem()

			# define the solution	
			v = np.array([float(v1), float(v2), float(v3)])
			if float(np.sum(v)) == 0:
				solution = 0
			else:
				prob = v/float(np.sum(v))
				solution = prob[v4]

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

