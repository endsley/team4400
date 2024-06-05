#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_javascript import st_javascript
from utils import *
import time


if __name__ == "__main__":
	st.set_page_config(
		page_title='ready',
		initial_sidebar_state="collapsed",
		page_icon="👋",
	)
	st.markdown( """<style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True)

	url = st_javascript("await fetch('').then(r => window.parent.location.href)")
	try:
		url = url.replace('registered', '')
		st.write("## You have registered, you can go to the login page at %s"%url)
	except:
		pass

