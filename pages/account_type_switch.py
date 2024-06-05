#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
import time

LOGGER = get_logger(__name__)

import asyncio
import time




if __name__ == "__main__":
	st.set_page_config(
		page_title="Hello",
		initial_sidebar_state="collapsed",
		page_icon="👋",
	)


	st.markdown( """<style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True,)
	if 'user_type' not in st.session_state:
		st.markdown(r''' ## This page does not exist... ''')
		st.stop()

	usrType = st.session_state['user_type']
	usrName = st.session_state['user_name']


	st.write("## Welcome %s"%usrName)
	st.write("Please pick the account view")

	clicked_1 = False
	clicked_2 = False
	clicked_3 = False


	if usrType == 7: clicked_1 = st.button('Root')
	if usrType > 4: clicked_2 = st.button('Teacher')
	if usrType > 0: clicked_3 = st.button('Student')

	while True:
		if clicked_1: switch_page("root_page")
		if clicked_2: switch_page("teachers_page")
		if clicked_3: 
			st.session_state['user_type'] = 1
			switch_page('students_page')
		time.sleep(1)

