#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
import time

LOGGER = get_logger(__name__)

import sqlite3
import asyncio
import time
import json


def display_problem(prob_title, prob_set_name):
	usr_name = st.session_state['name']
	st.session_state['course_problem_page'] = 'DS4400_problems'

	con = sqlite3.connect('account_info.db')
	cursorObj = con.cursor()
	result = cursorObj.execute('SELECT * FROM quiz_results where name="%s" and problem_name="%s"'%(usr_name, prob_set_name))
	result = cursorObj.fetchall()
	st.session_state['prob_name_list'] = json.loads(result[0][3])

	if len(result) == 0:
		old_score = 0
		num_times_complete = 0
	else:
		old_n = result[0][4]
		old_N = result[0][5]
		old_score = 100*old_n/old_N
		num_times_complete = result[0][6]

	col1, col2, col3, col4 = st.columns([1,1,1,1])
	review_click = False
	with col1:
		clicked = st.button(prob_title)
		#st.markdown('[%s](/%s)'%(prob_title, prob_set_name), unsafe_allow_html=True)
	with col2:
		if num_times_complete == 0:
			st.markdown('None')
		else:
			review_click = st.button('Review', key=prob_set_name)
	with col3:

		st.markdown('%d/%d=%.1f %%'%(old_n, old_N, old_score))
	with col4:
		st.markdown('%d'%num_times_complete)

	return clicked, review_click, old_score

if __name__ == "__main__":
	st.set_page_config(
		page_title="Hello",
		initial_sidebar_state="collapsed",
		page_icon="👋",
	)
	st.markdown( """<style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True,)
	st.write("## DS4400 Practice Problems")

	t1, t2, t3, t4= st.columns([1,1,1,1])
	with t1: st.markdown('#### Problem set')
	with t2: st.markdown('#### Review')
	with t3: st.markdown('#### Score')
	with t4: st.markdown('#### Attempts')

	matMult_click, review_click_1, old_score_1 = display_problem('Matrix Multiplication', 'problem_set_matrix_mult')
	matCalcA_click, review_click_2, old_score_2 = display_problem('Matrix Calculus A', 'problem_set_matrix_calculus_A')

	while True:
		if matMult_click: 
			st.session_state['score'] = old_score_1
			switch_page('problem_set_matrix_mult')
		if matCalcA_click: 
			st.session_state['score'] = old_score_2
			switch_page('problem_set_matrix_calculus_A')
		if review_click_1 or review_click_2:
			if review_click_1: curFname = 'problem_set_matrix_mult'
			elif review_click_2: curFname = 'problem_set_matrix_calculus_A'

			st.session_state['prob_num'] = 0
			st.session_state['initialization_page_ran'] = True
			st.session_state['starting_page_name'] = curFname
			switch_page(st.session_state['prob_name_list'][0]['fname'])

		time.sleep(1)


