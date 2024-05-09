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
	page_properly_initialized(4)

	deta = Deta(st.secrets["data_key"])
	db = deta.Base("classes")

	select_buttons = []
	uInfo = st.session_state['user_info']
	courses = []
	for eachAccount in uInfo:
		key = eachAccount['associated_course_key']
		course_info = db.fetch({'key':"%s"%key, "course_is_active":1}).items
		courses.append(course_info[0])

	rootView = False
	if st.session_state['user_type'] == 7: rootView = st.button('Back to Root View')
	st.write(' ## Welcome %s, here is a list of your courses.'%st.session_state['user_name'])
	t1, t2, t3, t4, t5, t6 = st.columns([1,1,1,1,1,1])
	
	with t1: st.write('**:blue[Name]**')
	with t2: st.write('**:blue[#Students]**')
	with t3: st.write('**:blue[#TAs]**')
	with t4: st.write('**:blue[Time]**')
	with t5: st.write('**:blue[Key]**')

	for i in courses:
		col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
		with col1: st.write(i['course_name'])
		with col2: st.write(len(i['student_list']))
		with col3: st.write(len(i['Teaching_assistant_list']))
		with col4: st.write(i['semester_year_session'])
		with col5: st.write(i['registration_key'])
		with col6: select_buttons.append((st.button('Enter', key=i['registration_key']), i['course_name'], i['registration_key'], i['semester_year_session'], i['key'], i['course_structure_key']))


	while True:
		for dB in select_buttons:
			if dB[0] == True:
				print(dB)
				st.session_state['registration_key'] = dB[2]
				st.session_state['course_key'] = dB[4]
				st.session_state['Time'] = dB[3]
				st.session_state['course_name'] = dB[1]
				st.session_state['course_structure_key'] = dB[5]
				switch_page("teacher_course_page")
		
		if rootView: switch_page("account_type_switch")
		time.sleep(1)


