#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
from deta import Deta
import time

LOGGER = get_logger(__name__)

import asyncio
import sqlite3
import time


if __name__ == "__main__":
	page_properly_initialized(1, title="ML", icon="👋", check_user_type=False)
	if 'end_session' in st.session_state: del st.session_state['end_session']

	st.markdown( """<style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True,)
	curFname, probList = get_all_problems(10, __file__)

	st.write('## Practice Questions for Matrix Multiplication')
	st.write('You can redo these questions as many times as you want!! Your final score will be the average of all scores!!')
	email = input_field('Email', key='emailEntry')
	pswd = input_field('password', key='pswdEntry3', type="password")
	clicked = st.button('Submit')

	while True:
		if clicked or 'pswd' in st.session_state: 
			if 'pswd' in st.session_state:
				email = st.session_state['user_email']
				pswd = st.session_state['pswd']

			deta = Deta(st.secrets["data_key"])
			db = deta.Base("accounts")
			user_info = db.fetch([{"email": email, "pswd": pswd}]).items
	
			if len(user_info) == 0:
				st.warning('User email and password pair does not exist', icon="⚠️")
				clicked = False
			else:
				stored_pswd = user_info[0]['pswd']
				if pswd == stored_pswd: 
					break
				else:
					st.warning('User email and password pair does not exist', icon="⚠️")
					clicked = False
		time.sleep(1)

	st.session_state['initialization_page_ran'] = True
	st.session_state['starting_page_name'] = curFname
	st.session_state['num_correct'] = 0
	st.session_state['prob_num'] = 0
	st.session_state['prob_name_list'] = probList
	switch_page(probList[0]['fname'])
