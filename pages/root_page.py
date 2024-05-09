#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from utils import *
import time

LOGGER = get_logger(__name__)

from deta import Deta
import sqlite3
import asyncio
import time




if __name__ == "__main__":
	page_properly_initialized(7, title="Chieh", icon="👋", check_user_type=False)

	BackView = st.button('Back')
	delete_buttons = []
	tab1, tab2 = st.tabs(["Teachers", "Courses"])	
	with tab1:
		deta = Deta(st.secrets["data_key"])
		db = deta.Base("accounts")
		result = db.fetch([{"user_type?gt": 3}]).items

		add_teacher_button = st.button('Add Teacher')
		t1, t2, t3 = st.columns([1,1,1])
		with t1: st.write('**:blue[Name]**')
		with t2: st.write('**:blue[Access]**')
		with t3: st.write('**:blue[Delete]**')

		for i in result:
			v = gen_random_string(str_len=5)
			col1, col2, col3 = st.columns([1,1,1])
			with col1: st.write(i['name'])
			with col2: st.write(i['user_type'])
			with col3: delete_buttons.append(st.button('Delete', key=v))
	with tab2:
		st.header("A dog")
		st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

	while True:
		if BackView: switch_page("account_type_switch")
		time.sleep(1)

