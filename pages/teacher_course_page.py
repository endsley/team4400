#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
import time
import pandas as pd
# from streamlit.server.server import Server

LOGGER = get_logger(__name__)

from deta import Deta
import sqlite3
import asyncio
import time




def display_problem(prob_title, prob_set_name, student_key):
	# if prob_set_name in st.session_state:
	# 	print(st.session_state)
	# 	quiz_results = st.session_state[prob_set_name]
	#
	# else:
	deta = Deta(st.secrets["data_key"])
	db = deta.Base("hw_test_results")
	quiz_results = db.fetch({'account_key': student_key, "problem_name": prob_set_name}).items
	# if quiz_results:
	# 	print(quiz_results[0]['account_name'])
	# account_name = db.fetch({'account_name': account_name})
	# st.session_state[prob_set_name] = quiz_results
	# print(quiz_results)

	if len(quiz_results) == 0:
		old_n = 0
		old_N = 0
		old_score = 0
		num_times_complete = 0
		account_name = 'N/A'
		stored_problem_list = get_all_problems(20, prob_set_name)
	else:
		old_n = quiz_results[0]['total_correct']
		old_N = quiz_results[0]['total_answered']
		account_name = quiz_results[0]['account_name']
		if old_N == 0:
			old_score = 0
		else:
			old_score = 100 * old_n / old_N
		num_times_complete = quiz_results[0]['total_completed']
		stored_problem_list = quiz_results[0]['latest_result_package']
	score = "%.1f" %(old_score)

	return clicked, old_score, stored_problem_list, quiz_results, account_name, score

if __name__ == "__main__":
	page_properly_initialized(4)
	structure_key = st.session_state['course_structure_key']
	course_key = st.session_state['course_key']
	timing = st.session_state['Time']
	course_name = st.session_state['course_name']

	teacherCourseView = st.button('Teacher Courses')
	st.write( r''' ## %s: %s'''%(course_name, timing))
	select_buttons = []
	hw_buttons = []
	tab1, tab2, tab3, tab4, tab5 = st.tabs(["Students", "Problem Sets", "Homework", "Tests", "Summary"])

	with tab1:
		deta = Deta(st.secrets["data_key"])
		class_db = deta.Base("classes")

		select_buttons = []
		course_info = class_db.fetch({'key':"%s"%course_key}).items[0]
		students = course_info['student_list']

		bt1, bt2 = st.columns([1,1])
		with bt1: add_teacher_button = st.button('Add Student')
		with bt2: delete_teacher_button = st.button('Delete Student')

		t1, t2, t3, t4, t5 = st.columns([2,1,1,1,1])
		with t1: st.write('**:blue[Email]**')
		with t2: st.write('**:blue[Name]**')
		with t3: st.write('**:blue[# Login]**')
		with t4: st.write('**:blue[ID]**')

		account_db = deta.Base("accounts")
		student_keys = account_db.fetch({'associated_course_key':course_key}).items

		# print(student_keys)
		for student in student_keys:
			#student = db.fetch({'key':"%s"%i}).items[0]
			col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])
			with col1: st.write(student['email'])
			with col2: st.write(student['name'])
			with col3: st.write(student['total_num_times_login'])
			with col4: st.write(student['NEU_ID'])
			with col5: select_buttons.append({'button':st.button('View', key=student['key']),  'email':student['email'], 'name':student['name'], 'course_key':course_key, 'student_key':student['key']})

	with tab2:
		deta = Deta(st.secrets["data_key"])
		course = deta.Base("course_structure")

		selected_buttons_tab2 = []
		structure_info = course.fetch({'key':"%s"%structure_key}).items[0]
		problem_list = structure_info['homework']
		bt1, bt2 = st.columns([1, 1])
		with bt1:
			add_question_button = st.button('Add Question')
		with bt2:
			delete_question_button = st.button('Delete Question')

		t1, t2 = st.columns([2, 1])
		if add_question_button:
			switch_page('Add_Question')
		with t1: st.write('**:blue[Problem Set]**')
		for problem in problem_list:
			col1, col2 = st.columns([2,1])
			with col1:st.write(problem[0])
			with col2:selected_buttons_tab2.append({'button':st.button('View', key = problem[1]), 'homework':problem[1], 'title': problem[0]})
		st.session_state['prev_hw_test_results'] = ''
		st.session_state['course_problem_page'] = 'teacher_course_page'
	with tab3:
		hw_test_results = deta.Base("hw_test_results")
		# student list stored in students
		# print('students:', students)
		selected_buttons_tab3 = []
		bt1, bt2 = st.columns([1, 1])
		with bt1:
			add_homework_button = st.button('Add Homework')
		with bt2:
			delete_homework_button = st.button('Delete Homework')

		t1, t2 = st.columns([4, 1])
		if add_homework_button:
			# Add Function Later
			pass
		with t1:
			st.write('**:blue[Homework Set]**')
		for i in range(len(problem_list)):
			problem = problem_list[i]
			st.session_state['problem'] = problem[1].split('_set_')[1]
			col1, col2, col3 = st.columns([2, 1, 2])
			with col1: clicked = st.button(problem[0], key = col1)
			with col2: publish = st.button('Publish', key = col2)
			with col3: export = st.button('Export Grades', key = problem[1] + "_button")
			if export:
				# student_scores = xlsxwriter.Workbook('scores.xlsx')
				student_list = []
				# worksheet = student_scores.add_worksheet()
				# row, col = 0, 0
				scores = []
				for student in students:
					doHW, prevScore, stored_problem_list, quiz_results, account_name, score = display_problem(problem[0], problem[1], student)
					# print(account_name, problem[1], score)
					# worksheet.write(row, col, account_name)
					student_list.append(account_name)
					scores.append(score)
					# worksheet.write(row, col + 1, score)
					# row += 1
				st.session_state['student_list'] = student_list
				st.session_state['scores'] = scores
				# student_scores.close()
				switch_page("export_scores")
				# st.experimental_rerun()


	with tab4:
		pass
	with tab5:
		pass

	while True:
		for dB in selected_buttons_tab2:
			if dB['button'] == True:
				# print(dB['homework'])
				st.session_state['starting_page_name'] = dB['homework']
				st.session_state['problem_set_title'] = dB['title']
				switch_page("problem_set_login")

		for dB in select_buttons:
			if dB['button'] == True:
				st.session_state['user_email'] = dB['email']
				st.session_state['user_name'] = dB['name']
				st.session_state['student_key'] = dB['student_key']
				st.session_state['course_info'] = course_info

				switch_page("student_course_page")

		if teacherCourseView: switch_page("teachers_page")
		if add_teacher_button: switch_page("student_registration")
		if delete_teacher_button: switch_page("delete_student")

		time.sleep(1)
