#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from deta import Deta
import time

LOGGER = get_logger(__name__)

import sqlite3
import asyncio
import time




if __name__ == "__main__":
	page_properly_initialized(1)
	select_buttons = []

	deta = Deta(st.secrets["data_key"])
	db = deta.Base("classes")

	registered_course_keys = []
	for account in st.session_state['user_info']: 
		registered_course_keys.append(account['associated_course_key'])

	#obtain all registered course info in a list
	if 'registered_courses' in st.session_state:
		registered_courses = st.session_state['registered_courses']
	else:
		registered_courses = []
		for key in registered_course_keys:
			course_info = db.fetch({'key':"%s"%key}).items
			registered_courses.append(course_info[0])

		st.session_state['registered_courses'] = registered_courses




	st.write(' ### **:black[Registered Courses for %s]**'%st.session_state['user_name'])
	t1, t2, t3, t4, t5 = st.columns([1,1,1,1,1])
	
	with t1: st.write('**:blue[Name]**')
	with t2: st.write('**:blue[#Students]**')
	with t3: st.write('**:blue[#TAs]**')
	with t4: st.write('**:blue[Time]**')

	for i in registered_courses:
		col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
		with col1: st.write(i['course_name'])
		with col2: st.write(len(i['student_list']))
		with col3: st.write(len(i['Teaching_assistant_list']))
		with col4: st.write(i['semester_year_session'])
		with col5: select_buttons.append((st.button('Enter', key=i['registration_key']), i))

	while True:
		for dB in select_buttons:
			if dB[0] == True:
				st.session_state['course_info'] = dB[1]
				switch_page("student_course_page")
		
		time.sleep(1)

