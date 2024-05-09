#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
import time
import pdb
LOGGER = get_logger(__name__)

from deta import Deta
import json
import sqlite3
import asyncio
import time


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
	deta = Deta(st.secrets["data_key"])

	# renew the course info each time 
	course_info = st.session_state['course_info']
	classes_db = deta.Base("classes")
	course_info = classes_db.fetch({'key':course_info['key']}).items[0]
	#-------------------------------

	teacherV = False
	studentV = False
	st.session_state['course_problem_page'] = 'student_course_page'
	if st.session_state['user_type'] > 3: teacherV = st.button('Course View', key='TeacherCourseView')
	if st.session_state['user_type'] == 1: studentV = st.button('Course View', key='studentCourseView')

	st.write( r''' ## %s %s'''%(course_info['course_name'], course_info['semester_year_session']))
	hw_buttons = []
	tab1, tab2, tab3, tab4 = st.tabs(["Homework", "Tests", "Stats", "Info"])	
	with tab1:
		key = course_info['course_structure_key']
		db = deta.Base("course_structure")
		course_struct = db.fetch({'key':"%s"%key}).items[0]
		HW = course_struct['homework']

		t1, t2, t3, t4= st.columns([1,1,1,1])
		with t1: st.markdown('**:blue[Problem set]**')
		with t2: st.markdown('**:blue[Review]**')
		with t3: st.markdown('**:blue[Score]**')
		with t4: st.markdown('**:blue[Attempts]**')
	
		for ps in HW:
			doHW, rwHW, prevScore, stored_problem_list, quiz_results = display_problem(ps[0], ps[1])
			single_hw = [doHW, rwHW, prevScore, ps[0], ps[1], stored_problem_list, quiz_results]
			hw_buttons.append(single_hw)

		while True:
			for hw in hw_buttons:
				if hw[0]: 
					st.session_state['score'] = hw[2]
					st.session_state['problem_set_title'] = hw[3]
					st.session_state['prev_hw_test_results'] = hw[6]
					st.session_state['starting_page_name'] = hw[4]
					del st.session_state[hw[4]]		# delete the cache


					switch_page('problem_set_login')
				elif hw[1]: 
					st.session_state['prev_hw_test_results'] = hw[6]
					st.session_state['starting_page_name'] = hw[4]
					st.session_state['problem_set_title'] = hw[3]
					st.session_state['prob_name_list'] = hw[5]
					# pdb.set_trace()
					st.session_state['prob_num'] = 0
					st.session_state['initialization_page_ran'] = True
					switch_page(st.session_state['prob_name_list'][0]['fname'])

					#st.write('--------------------------')
					#st.write(st.session_state['prev_hw_test_results'])
					#time.sleep(10)

			if teacherV: 
				for ps in HW: clear_session_variables(var_list=[ps[1]])		# remove problem sets if go back to teach view cus it can view another student
				switch_page('teacher_course_page')

			if studentV:
				switch_page('students_page')

			time.sleep(1)


