#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
import time

LOGGER = get_logger(__name__)

from deta import Deta
import asyncio
import time




if __name__ == "__main__":
	page_properly_initialized(1, check_user_type=False)

	goback = st.button('go back')
	st.write("## Delete Student")
	email = input_field('Student email', key='email')
	clicked = st.button('Submit')

	while True:
		time.sleep(1)
		if goback:
			switch_page("teacher_course_page")
		elif clicked:
			st.warning('Please wait a sec as we delete the account.', icon="⚠️")
			deta = Deta(st.secrets["data_key"])
			account_db = deta.Base("accounts")
			student_account = account_db.fetch([{"email": email}]).items
	
			if len(student_account) == 0:
				st.error('This student email does not exist', icon="🚨")
				clicked = False
			else:
				clicked = False
				key = student_account[0]['key']
				course_key = st.session_state['course_key']

				classes_db = deta.Base("classes")
				course = classes_db.fetch({"key": course_key}).items

				# Remove student from class student_list
				try: 
					course[0]['student_list'].remove(key)
					updates = {'student_list':course[0]['student_list']}
					classes_db.update(updates, course_key)

				except: pass

				# remove the student record from quizes
				hw_test_db = deta.Base("hw_test_results")
				all_hws = hw_test_db.fetch({"account_key": key}).items
				for i in all_hws:
					hw_test_db.delete(i['key'])

				# delete the actual account
				account_db.delete(student_account[0]['key'])
				st.warning('Deletion successful.', icon="⚠️")

