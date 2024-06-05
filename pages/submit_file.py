#!/usr/bin/env python

import streamlit as st
from streamlit.logger import get_logger
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from deta import Deta
from utils import *
from pathlib import Path
import time

import subprocess
import os

LOGGER = get_logger(__name__)

import sqlite3
import asyncio
import time
import pickle
import json

import sys



if __name__ == "__main__":
	page_properly_initialized(1)

	st.write("## Submit File")


	python_file = st.file_uploader("Upload Python File", type = ['py'])


	clicked = st.button('Upload')
	# clicked = False

	if python_file is not None:
		if 'data' not in st.session_state:
			st.session_state['data'] = 0
		data = python_file.getvalue().decode('utf-8')
		st.write(data)
		st.session_state['data'] = data


		if clicked:
			# UPLOAD FILE

			data = st.session_state['data']
			parent_path = Path(__file__).parent.parent.resolve()
			save_path = os.path.join(parent_path, "pages")
			complete_name = os.path.join(save_path, 'uploaded_file.py')
			destination_file = open(complete_name, "w")
			destination_file.write(data)
			destination_file.close()
			# print(st.session_state[prob_set_name])
			st.session_state['num_correct'] = 0
			st.session_state['preview'] = 1
			st.session_state['prob_num'] = 0
			st.session_state['prob_name_list'] = [{'fname': 'uploaded_file', 'input': None, 'solution': None, 'response': None}]

			switch_page('uploaded_file')
