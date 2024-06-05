#!/usr/bin/env python
import os
import streamlit as st
from streamlit.logger import get_logger
from streamlit_extras.switch_page_button import switch_page
from utils import *
import time

LOGGER = get_logger(__name__)

from deta import Deta
import json
import asyncio
import sqlite3
import time



if __name__ == "__main__":
	page_properly_initialized(1)
	start_page = st.session_state['starting_page_name']
	print(start_page)
	st.write('## Finished')
	n = st.session_state['num_correct']
	N = len(st.session_state['prob_name_list'])
	if 'preview' not in st.session_state or st.session_state['preview'] == 0:
		st.markdown( """For this problem set got %d out of %d problems correct. With a score of %.3f"""%(n, N, n/N))

	prev_hw_test_results = st.session_state['prev_hw_test_results']

	if 'end_session' not in st.session_state:
		deta = Deta(st.secrets["data_key"])
		db = deta.Base("hw_test_results")

		if len(prev_hw_test_results) == 0:
			key = gen_random_string(str_len=13)
			updates = {
				"key": key,
				"account_key": st.session_state['account_key'],
				"account_name": st.session_state['user_name'],
				"latest_result_package": st.session_state['prob_name_list'],
				"problem_name": st.session_state['starting_page_name'],
				"total_answered": N,
				"total_completed": 1,
				"total_correct": n
			}
			db.put(updates)
			#print('ran A -------------\n\n\n')
		else:
			prev_hw_test_results = prev_hw_test_results[0]
			old_n = prev_hw_test_results['total_correct']
			old_N = prev_hw_test_results['total_answered']
			if old_N == 0: old_score = 0
			else: old_score = old_n/old_N
			num_completed = prev_hw_test_results['total_completed'] + 1

			if n/N > old_score:
				new_score = (old_n+n)/(old_N+N)
				st.markdown( """Your score has improved from %.3f to %.3f"""%(old_score, new_score))

				updates = {
					"latest_result_package": st.session_state['prob_name_list'],
					"total_answered": old_N+N,
					"total_completed": num_completed,
					"total_correct": old_n+n
				}

				db.update(updates, prev_hw_test_results['key'])
				#print('ran B -------------\n\n\n')
			else:
				st.markdown( """Your score did not improve and remained unchanged at %.3f"""%(old_score))

				updates = {
					"latest_result_package": st.session_state['prob_name_list'],
					"total_answered": old_N,
					"total_completed": num_completed,
					"total_correct": old_n
				}
				db.update(updates, prev_hw_test_results['key'])
				#print('ran C -------------\n\n\n')


	if st.session_state['preview'] == 1:
		st.write('File Uploaded Successfully!')
		current_directory = os.getcwd() + "/pages"
		old_filename = 'uploaded_file.py'
		new_filename = f"{st.session_state['prob_set_name']}_{st.session_state['prob_num']}.py"

		old_filepath = os.path.join(current_directory, old_filename)
		new_filepath = os.path.join(current_directory, new_filename)
		clicked_1 = st.button('Add More Questions')
		clicked_2 = st.button('Go back to Main Problem set Page')

		# Check if the old file exists before attempting to rename
		if os.path.exists(old_filepath):
			os.rename(old_filepath, new_filepath)
			st.session_state['preview'] = 0
		if clicked_1:
			st.session_state['end_session'] = True
			switch_page('submit_file')
		if clicked_2:
			st.session_state['end_session'] = True
			switch_page(st.session_state['course_problem_page'])


		else:
			print(f"File '{old_filepath}' does not exist.")

	else:
		st.session_state['end_session'] = True
		clicked_1 = st.button('Review Problem set')
		clicked_2 = st.button('Try again')
		clicked_4 = st.button('Go back to Main Problem set Page')


		while True:
			if clicked_1:
				st.session_state['prob_num'] = 0
				clear_session_variables()

				#st.write(st.session_state['prob_name_list'])
				#time.sleep(10)

				switch_page(st.session_state['prob_name_list'][0]['fname'])
				break
			if clicked_2:
				clear_session_variables()
				switch_page('problem_set_login')
				#switch_page(start_page)
				break
			if clicked_4:
				clear_session_variables()
				switch_page(st.session_state['course_problem_page'])
				break

			time.sleep(1)





	#st.markdown( """The current best score is """)
	#st.markdown( """The current worst score is """)


	#col1, col2 = st.columns([1,1])
	#with col1:
	#	clicked_1 = st.button('Review Problem set')
	#with col2:
	#	clicked_2 = st.button('Try again')
