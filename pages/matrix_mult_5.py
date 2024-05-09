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
			[v1,v2,v3,v4,v5,v6,v7,v8,v9,v10, v11] = retrieve_display_variables()
			display_new_line(r''' 
				$$ 
				\begin{bmatrix} %d & %d \\ %d & %d \\ %d & %d \end{bmatrix}
				\begin{bmatrix} %d & %d \\ %d & %d \end{bmatrix}
				= 
				\begin{bmatrix} a & b \\ c & d \\ e & f \end{bmatrix}
				$$ 
				''',(v1,v2,v3,v4,v5,v6,v7,v8,v9,v10))
			display_new_line('What is %s ?', (v11))


		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			[v1 ,v2 ,v3 ,v4 ,v5 ,v6 ,v7 ,v8 ,v9 ,v10] = getMultInts(10, -3, 3)
			v11 = getInt(0,5,'v11')
			L = ['$a$' ,'$b$' ,'$c$' ,'$d$' ,'$e$' ,'$f$']

			# define key variables and display the problem
			set_page_variables_for_display([v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,L[v11]])
			display_problem()

			# define the solution	
			a = np.array([[v1, v2],[v3, v4],[v5, v6]])
			b = np.array([[v7, v8],[v9,v10]])
			AB = a.dot(b)
			AB = np.reshape(AB, (1,6))
			solution = AB[0][v11]

			params = problem_display_ending(solution, 'number')

		return params

	standard_problem_page(n_sec, display)

