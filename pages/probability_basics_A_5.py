#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import pandas as pd
#from pandas.compat import StringIO
from io import StringIO
import time

if __name__ == "__main__":
	n_sec = 50

	#	This question tests marginal probability
	def display():
		#	Define this function for new problem
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[v1, L] = retrieve_display_variables()
			v1 = pd.read_csv(StringIO(v1), header=0, index_col=0)	# convert string back into dataFrame

			display_new_line(r'''Given the following table''')
			st.write(v1)
			display_new_line(r'''what is %s?''',(L))

		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			dx = 2
			dy = 3
			v1 = get_random_joint_distribution_table(x_dim=dx, y_dim=dy, sessionID='v1')
			v2 = getInt(0,dx-1, sessionID='v2')
			v3 = getInt(0,dy-1, sessionID='v3')
			v4 = getInt(0,1, sessionID='v4')
			
			if v4 == 0: L = 'p(x=%d)'%v2 
			else: L = 'p(y=%d)'%v3 

			# define key variables and display the problem
			set_page_variables_for_display([v1.to_csv(), L])	# dataframe can only be transported as string
			display_problem()

			# define the solution	
			P = v1.to_numpy()
			if v4 == 0: solution = np.sum(P, axis=0)[v2]
			else: solution = np.sum(P, axis=1)[v3]	

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

