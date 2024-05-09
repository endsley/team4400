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
	page_properly_initialized(1, title=st.session_state['problem_set_title'], icon="⭐")
	if 'end_session' in st.session_state: del st.session_state['end_session']

	curFname, probList = get_all_problems(20, st.session_state['starting_page_name'])
#	print('\nkkkk\n', st.session_state['starting_page_name'], '\nkkkk\n')
#	print(curFname)
#	print('\n\n')
#	print(probList)

	st.write('## Practice Questions for ' + st.session_state['problem_set_title'])
	st.write('You can redo these questions as many times as you want!! If you get a higher score, it will be averaged into the total. If you get a worse score, it will be ignored. So you can only improve.')
	email = input_field('Email', key='emailTmp')
	pswd = input_field('password', key='passwordTmp', type="password")
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
				#time.sleep(20)
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
	#print(probList[0]['fname'])
	switch_page(probList[0]['fname'])
