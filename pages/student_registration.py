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

	goBack = False
	if 'user_type' in st.session_state:
		if st.session_state['user_type'] > 3: goBack = st.button('go Back')

	st.write("## Student Course Registration")
	email = input_field('Email', key='email')
	name = input_field('Name', key='name')
	pswd = input_field('password', type="password", key='pswd')
	neuID = input_field('University ID', key='neuid')
	registration_key = input_field('Course Key', key='ckey')
	clicked = st.button('Submit')

	while True:
		time.sleep(1)
		if goBack:
			switch_page("teacher_course_page")
		elif clicked:
			st.warning('Please wait while we create your account.', icon="⚠️")
			deta = Deta(st.secrets["data_key"])
			class_db = deta.Base("classes")
			course = class_db.fetch([{"registration_key": registration_key}]).items
	
			if len(course) == 0:
				st.error('This course key does not exist', icon="🚨")
				clicked = False
			else:
				account_db = deta.Base("accounts")
				account = account_db.fetch({"email": email}).items

				if len(account) == 0:
					key = gen_random_string(str_len=13)
					newAccount = {
						"key": key,
						"NEU_ID": neuID,
						"account_expiration_date": "never",
						"associated_course": course[0]['course_name'],
						"associated_course_key": course[0]['key'],
						"email": email,
						"name": name,
						"num_students": 0,
						"pswd": pswd,
						"registration_key": registration_key,
						"semester_year_session": course[0]['semester_year_session'],
						"total_num_times_login": 0,
						"user_type": 1
					}
					account_db.insert(newAccount)

					#	add the student to the student_list of the class
					course[0]['student_list'].append(key)
					class_db.update({'student_list':course[0]['student_list']}, course[0]['key'])
					switch_page("registered")


				else:
					st.error('This email account already exists, you can add a new class in your account.', icon="🚨")
					clicked = False


		time.sleep(1)


