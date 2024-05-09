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
			display_new_line(r'''Given $n$ samples, the derivative of ''')
			display_new_line(r'''$$f(w) = \frac{1}{2} \sum_{i=1}^n (w^T x_i - y_i)^2 + s||w||_2 + t||w||_1$$''')
			display_new_line(r'''is''')
			display_new_line(r'''%s''',(v1))
			display_new_line(r'''what is ❓''')
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			# generate random data
			v1 = getInt(0,10,'v1')
			L = [    r"$$\nabla f(w) =  ❓\sum_{i=1}^n (w^T x_i - y_i) x_i + s \frac{w}{||w||_2} + t sign(w)$$"]
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^❓ (w^T x_i - y_i) x_i + s \frac{w}{||w||_2} + t sign(w)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (❓^T x_i - y_i) x_i + s \frac{w}{||w||_2} + t sign(w)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (w^T ❓_i - y_i) x_i + s \frac{w}{||w||_2} + t sign(w)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (w^T x_i - ❓_i) x_i + s \frac{w}{||w||_2} + t sign(w)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (w^T x_i - y_i) ❓_i + s \frac{w}{||w||_2} + t sign(w)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (w^T x_i - y_i) x_i + s \frac{w}{||❓||_2} + t sign(w)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (w^T x_i - y_i) x_i + s \frac{w}{||w||_❓} + t sign(w)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (w^T x_i - y_i) x_i + s \frac{w}{||w||_2} +  t sign(❓)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (w^T x_i - y_i) x_i + ❓ \frac{w}{||w||_2} + t sign(w)$$")
			L.append(r"$$\nabla f(w) =  \sum_{i=1}^n (w^T x_i - y_i) x_i + s \frac{w}{||w||_2} + ❓ sign(w)$$")
			L2 = ['1', 'n', 'w', 'x', 'y', 'x', 'w', '2', 'w', 's', 't']

			# define key variables and display the problem
			set_page_variables_for_display([L[v1]])
			display_problem()

			# define the solution	
			solution = L2[v1]
			params = problem_display_ending(solution, 'text')

		return params

	standard_problem_page(n_sec, display)

