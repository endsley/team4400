#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
import random
from math import isclose
import time

if __name__ == "__main__":
	n_sec = 60


	def display():
		#	Define this function for new problem
		def display_problem():
			display_color_problem_title()

			#	parts where you change
			[a, b, c, d, e, v1] = retrieve_display_variables()
			display_new_line(r'''You were around campus and asked what most students are worried about, and you got''')
			display_new_line(r'''$$ %d $$ people $$ x_{1} $$: Job after college''', a)
			display_new_line(r'''$$ %d $$ people $$ x_{2} $$: Family and friends issues''', b)
			display_new_line(r'''$$ %d $$ people $$ x_{3} $$: Grades''', c)
			display_new_line(r'''$$ %d $$ people $$ x_{4} $$: Love life''', d)
			display_new_line(r'''$$ %d $$ people $$ x_{5} $$: Others''', e)
			display_new_line(r'''Given X = $$ \begin{bmatrix} x1 & x2 & x3 & x4 & x5 \end{bmatrix}^T$$, choose the equation for $$p(x)$$.''',)

			display_multiple_choice(v1)
		# -------------------------------------------------------------------

		if problem_has_been_answered():
			display_problem()
			params = display_solutions()
		else:
			a = np.round((getInt(100, 300)) / 100) * 100# round to the nearest int divisible by 100
			b = np.round((getInt(100, 300)) / 100) * 100
			c = np.round((getInt(100, 300))/ 100) * 100
			d = np.round((getInt(100, 300)) / 100) * 100
			e = np.round((getInt(100, 300)) / 100) * 100
			summation = a + b + c + d + e
			v1 = multiple_choice([rf'''$$ \frac{{1}}{{{int(summation)}}}[{int(a)}^{{x_{1}}}*{int(b)}^{{x_{2}}}*{int(c)}^{{x_{3}}}*{int(d)}^{{x_{4}}}*{int(e)}^{{x_{5}}}] $$''',
								rf'''$$ \frac{{1}}{{{int(summation)}}}[{int(a)}^{{x_{1}}} + {int(b)}^{{x_{2}}} + {int(c)}^{{x_{3}}} + {int(d)}^{{x_{4}}} + {int(e)}^{{x_{5}}}] $$''',
								  rf'''$$ \frac{{1}}{{{int(summation)}}}[{{x_{1}}}^{{{int(a)}}} + {{x_{2}}}^{{{int(b)}}} + {{x_{3}}}^{{{int(c)}}} + {{x_{4}}}^{{{int(d)}}} + {{x_{5}}}^{{{int(e)}}}] $$''',
								  rf'''$$ \frac{{1}}{{{int(summation)}}}[{{x_{1}}}^{{{int(a)}}}*{{x_{2}}}^{{{int(b)}}}*{{x_{3}}}^{{{int(c)}}}*{{x_{4}}}^{{{int(d)}}}*{{x_{5}}}^{{{int(e)}}}] $$'''],'v1')

			set_page_variables_for_display([a, b, c, d, e, v1])
			display_problem()

			# define the solution
			solution = v1[0]
			params = problem_display_ending(solution, 'text')

			if 'preview' in st.session_state and st.session_state['preview'] == 1:
				st.write("Solution is: " + str(solution))

		return params

	standard_problem_page(n_sec, display)


