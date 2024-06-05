#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from utils import *
import time

LOGGER = get_logger(__name__)

import sqlite3
import asyncio
import time
import pickle
import json

def display_problem(prob_title, prob_set_name):
	if prob_set_name in st.session_state:
		quiz_results = st.session_state[prob_set_name]
	else:
		deta = Deta(st.secrets["data_key"])
		db = deta.Base("hw_test_results")
		quiz_results = db.fetch({'account_key':st.session_state['student_key'], "problem_name": prob_set_name}).items
		st.session_state[prob_set_name] = quiz_results
	if len(quiz_results) == 0:
		old_n = 0
		old_N = 0
		old_score = 0
		num_times_complete = 0
		stored_problem_list = get_all_problems(20, prob_set_name)
	else:
		old_n = quiz_results[0]['total_correct']
		old_N = quiz_results[0]['total_answered']
		if old_N == 0: old_score = 0
		else: old_score = 100*old_n/old_N
		num_times_complete = quiz_results[0]['total_completed']
		stored_problem_list = quiz_results[0]['latest_result_package']

	col1, col2, col3, col4 = st.columns([1,1,1,1])
	review_click = False
	with col1:
		if st.session_state['user_type'] == 1: clicked = st.button(prob_title)
		else:
			clicked = False
			st.markdown('**:green[%s]**'%prob_title)
	with col2:
		if num_times_complete == 0:
			st.markdown('None')
		else:
			review_click = st.button('Review', key=prob_set_name + "_button")
	with col3:
		st.markdown('%d/%d=%.1f %%'%(old_n, old_N, old_score))
	with col4:
		st.markdown('%d'%num_times_complete)

	return clicked, review_click, old_score, stored_problem_list, quiz_results



if __name__ == "__main__":
	page_properly_initialized(1)

	st.write("## Adding New Questions")
	addQkey = input_field('Add Question Key', key='addQkey')
	module = input_field('Module', columns=None, key='homework')
	clicked = st.button('Submit')

	while True:
		if clicked:
			deta = Deta(st.secrets["data_key"])
			db = deta.Base("course_structure")
			user_info = db.fetch([{"addQkey": addQkey}]).items
			if len(user_info) == 0:
				st.warning('Incorrect Key', icon="⚠️")
				clicked = False
			else:
				flag = 0
				HW = user_info[0]['homework']
				for hw in HW:
					if module == hw[0]:
						st.session_state['prob_name_list'] = hw[1]
						flag = 1
						break
				if flag == 0:
					st.warning('Module does not exist', icon="⚠️")
					clicked = False
				if flag == 1:
					prob_set_name = hw[1][12:]
					st.session_state['prob_set_name'] = prob_set_name
					st.session_state['starting_page_name'] = prob_set_name
					st.session_state[prob_set_name] = prob_set_name
					st.session_state['prev_hw_test_results'] = ''
					st.session_state['module_title'] = prob_set_name
					stored_problem_list = get_all_problems(20, hw[1])
					st.session_state['length'] = len(stored_problem_list[1])
					# print(st.session_state['length'])
					switch_page('submit_file')
		time.sleep(1)
