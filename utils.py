# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import string
import streamlit as st
import inspect
import textwrap
import os
from streamlit_extras.switch_page_button import switch_page
from streamlit_javascript import st_javascript		# pip install streamlit-javascript
import time
import random
from math import isclose
import numpy as np
import pandas as pd
from copy import deepcopy
from sklearn.preprocessing import normalize
from sympy import *

#from streamlit_js_eval import get_page_location



#from pathlib import Path
from streamlit.source_util import (
	page_icon_and_name,
	calc_md5,
	get_pages,
	_on_pages_changed
)

def check_page_in_listing(page_name):
	current_pages = get_pages('./pages')

	for key, value in current_pages.items():
		if value['page_name'] == page_name:
			return True

	return False

def remove_all(remove_list, rm_item):
	try:
		while True: remove_list.remove(rm_item)
	except:
		return remove_list

def keep_these_pages_in_side_bar(page_names):

	current_pages = get_pages('./pages')
	current_pages_copy = deepcopy(current_pages)
	st.session_state['original_pages'] = current_pages_copy

	for key, value in current_pages_copy.items():
		if value['page_name'] not in page_names:
			del current_pages[key]

	_on_pages_changed.send()



def delete_page_from_side_bar(main_script_path_str, page_name):

	current_pages = get_pages(main_script_path_str)

	for key, value in current_pages.items():
		if value['page_name'] == page_name:
			del current_pages[key]
			break
		else:
			pass
	_on_pages_changed.send()

def problem_has_been_answered():
	probList = st.session_state['prob_name_list']
	currentID = st.session_state['prob_num']
	if 'correct' in probList[currentID]:
		return True
	else:
		return False

def display_solutions(additional_display=None):
	currentID = st.session_state['prob_num']

	probList = st.session_state['prob_name_list']
	solution = probList[currentID]['solution']
	response = probList[currentID]['response']

	if response == '': response = '(did not provide a response)'
	st.code('Your response is %s\nThe correct solution is %s'%(response, solution), language='python')

	if additional_display is not None: st.markdown(additional_display)
	params = [solution, response, []]
	return params


def display_new_line(line, variables=None):
	if variables is None:
		st.markdown(line)
	else:
		try:
			st.markdown(line%variables)
		except:
			line = line.replace('%d','%s')
			st.markdown(line%variables)

def display_color_problem_title(correct=None, prob_id=None, numProbs=None):
	probList = st.session_state['prob_name_list']
	currentID = st.session_state['prob_num']

	if problem_has_been_answered():
		correct = probList[currentID]['correct']

	if numProbs is None:
		numProbs = len(probList)
		prob_id = st.session_state['prob_num'] + 1

	if correct:
		st.markdown(r''' ### :green[Problem %d out of %d is Correct]'''%(prob_id, numProbs))
	elif correct is None:
		st.markdown(r'''## Problem %d out of %d'''%(prob_id, numProbs))
	else:
		st.markdown(r''' ### :red[Problem %d out of %d is Incorrect]'''%(prob_id, numProbs))

def clear_session_variables(var_list=[]):
	for var in var_list:
		if var in st.session_state:
			del st.session_state[var]

	if 'page_global_variables' in st.session_state:
		del st.session_state['page_global_variables']

	if 'page_displayed_already' in st.session_state:
		del st.session_state['page_displayed_already']

	if 'page_specific_key' in st.session_state:
		for var in st.session_state['page_specific_key']:
			if var in st.session_state:
				del st.session_state[var]

	for var in ['v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11']:
		if var in st.session_state:
			del st.session_state[var]


def get_random_joint_distribution_table(x_dim=2, y_dim=3, sessionID=None):
	if sessionID is not None:
		if sessionID in st.session_state:
			return st.session_state[sessionID]

	Y = np.round(np.random.rand(1, x_dim),1)
	Y = np.round(Y/np.sum(Y), 2)
	err = 1 - np.sum(Y)
	Y[0] = Y[0] + err


	X = np.round(np.random.rand(y_dim, x_dim),1)
	X = np.round(normalize(X, axis=0, norm='l1'),2)
	d = np.array([1,1]) - np.sum(X,axis=0)
	X[0,:] = X[0,:] + d

	Z = np.round(X*Y, 2)

	cname = []
	yname = []
	for i, j in enumerate(range(x_dim)): cname.append( 'x=%d'%i)
	for i, j in enumerate(range(y_dim)): yname.append( 'y=%d'%i)

	df = pd.DataFrame(Z, columns=cname, index=yname)

	if sessionID is not None:
		st.session_state[sessionID] = df
		add_page_specific_session_id(sessionID)

	return df



def generate_random_rref(i, j, sessionID=None):
	if sessionID is not None:
		if sessionID in st.session_state:
			return st.session_state[sessionID]

	in_or_not = np.random.randint(0, high=2)	# 0=not in, 1 = in
	M = Matrix(np.random.randint(-8, high=8, size=(i,j), dtype='l'))
	M_rref = M.rref()
	rref = M_rref[0]
	pivot = M_rref[1]
	properValues = []

	for i in rref:
		if type(i).__name__ == 'Rational' or type(i).__name__ == 'Integer':
			properValues.append(i)

	if in_or_not == 0 or len(properValues) == 0:	# not inside
		search_for_good_one = True
		in_or_not = 0
		while search_for_good_one:
			search_for_good_one = False
			numerator = np.random.randint(-100, high=100)
			denominator = np.random.randint(-100, high=100)
			value = Rational(numerator, denominator)
			if len(properValues) != 0:
				for pV in properValues:
					if value == pV:	# if just 1 value is the same repeat.
						search_for_good_one = True
	else:
		value = random.choice(properValues)

	original_matrix = '$' + latex(M).replace('\\left[','').replace('\\right]','').replace('matrix','bmatrix') + '$'
	final_rref = '$' + latex(rref).replace('\\left[','').replace('\\right]','').replace('matrix','bmatrix') + '$'
	value = str(value)

	output = [in_or_not, original_matrix, final_rref, value]
	if sessionID is not None:
		st.session_state[sessionID] = output
		add_page_specific_session_id(sessionID)

	return output




def gen_random_string(str_len=5, letters=string.ascii_letters):
	return ''.join(random.choice(letters) for i in range(str_len))


def getRandEmoji(sessionID=None, ignor_list=[]):
	if sessionID is not None:
		if sessionID in st.session_state:
			return st.session_state[sessionID]

	Remoj = ['🌰' ,'🌱' ,'🌲' ,'🌳' ,'🌴' ,'🌵' ,'🌶️' ,'🌷' ,'🌸' ,'🌹' ,'🌺' ,'🌻' ,'🌼' ,'🌽' ,'🌾' ,'🌿' ,'🍀' ,'🍁' ,'🍂' ,'🍃' ,'🍄' ,'🍅' ,'🍆' ,'🍇' ,'🍈' ,'🍉' ,'🍊' ,'🍋']
	for i in ignor_list:
		Remoj.remove(i)
	random.shuffle(Remoj)

	if sessionID is not None:
		st.session_state[sessionID] = Remoj[0]
		add_page_specific_session_id(sessionID)
	return Remoj[0]




def getRandLetter(sessionID=None, letter_type='lower_case', ignore_letters=[]):
	if sessionID is not None:
		if sessionID in st.session_state:
			return st.session_state[sessionID]

	if letter_type == 'lower_case':
		L = string.ascii_lowercase
	elif letter_type == 'upper_case':
		L = string.ascii_uppercase
		#outV = random.choice(string.ascii_uppercase)
	elif letter_type == 'all_cases':
		L = string.ascii_letters
		#outV = random.choice(string.ascii_letters)

	for i in ignore_letters: L = L.replace(i, '')
	outV = random.choice(L)

	if sessionID is not None:
		st.session_state[sessionID] = outV
		add_page_specific_session_id(sessionID)
	return outV

def add_page_specific_session_id(key_value):
	if 'page_specific_key' in st.session_state:
		st.session_state['page_specific_key'].append( key_value )
	else:
		st.session_state['page_specific_key'] = [key_value ]

def getMultInts(n, minV,maxV):
	var = []
	for i in range(n):
		sessionKey = 'v'+str(i+1)
#		if sessionKey in st.session_state:
#			raise ValueError('\n\n\nTingting, you can only call getMultInts once in a page. It has to do with some internal memory issue which I have not fix. We will eventually fix this, but for now, only call it once, then uset getInt function.\n\n\n')

		var.append(getInt(minV,maxV, sessionID=sessionKey))		# Kayla, its very important that you don't mess up the session ID, ask me when you get here
		add_page_specific_session_id(sessionKey)

	return var


def getInt(minV,maxV, sessionID=None):
	if sessionID is not None:
		if sessionID in st.session_state:
			return st.session_state[sessionID]

	random.seed()
	outV = random.randint(minV,maxV)

	if sessionID is not None:
		st.session_state[sessionID] = outV
		add_page_specific_session_id(sessionID)
	return outV

def display_multiple_choice(choices):
	S = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
	print('\n\n', type(choices))
	print('\n\n', choices[2])
	#st.write(type(choices))
	for i, j in enumerate(choices[2]):
		st.write(S[i] + ': ' + j)


def multiple_choice(choices, sessionID=None):
	if sessionID is not None:
		if sessionID in st.session_state:
			return st.session_state[sessionID]

	S = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789'
	answer = choices[0]
	random.shuffle(choices)
	lime_pos = choices.index(answer)

	if sessionID is not None:
		st.session_state[sessionID] = [S[lime_pos], answer, choices]
		add_page_specific_session_id(sessionID)


	return [S[lime_pos], answer, choices]



def page_properly_initialized(user_type, title='Hello', icon="👋", check_user_type=True):
	st.set_page_config(
		page_title=title,
		initial_sidebar_state="collapsed",
		page_icon=icon,
	)
	st.markdown( """<style> [data-testid="collapsedControl"] { display: none } </style> """, unsafe_allow_html=True)

	if check_user_type:
		if 'user_type' in st.session_state and 'user_name'  in st.session_state: pass
		else:
			st.markdown(r''' ## This page is missing process info, please sign in again... ''')
			st.stop()

		if wrong_user_type(user_type):
			st.stop()

#	This prevents a back button press
def problem_set_page_properly_initialized():

	probList = st.session_state['prob_name_list']
	currentID = st.session_state['prob_num']

	frame = inspect.stack()[2]
	module = inspect.getmodule(frame[0])
	key = module.__file__.strip('.py').split('/')[-1]

	print(st.session_state['prob_num'], probList[0]['fname'], key)
	if probList[currentID]['fname'] != key:
		st.markdown(r''' ## Error: This is a web app, you cannot press the back button !!! Please log in again.''')
		st.stop()

def standard_problem_page(n_sec, display_code):
	page_properly_initialized(1, title="Problem set", icon="❓")
	problem_set_page_properly_initialized()

	if 'current_sec' in st.session_state: n_sec = st.session_state['current_sec']

	probList = st.session_state['prob_name_list']
	currentID = st.session_state['prob_num']

	if 'correct' in probList[currentID]:
		prevButton = False
		nextButton = False

		colA, colB = st.columns([1,1])
		with colA: tryAgain = st.button('Try Again')
		with colB: exitButton = st.button('Exit')

		params = display_code()

		col1, col2 = st.columns([1,1])
		if currentID != 0:
			with col1: prevButton = st.button('Previous Problem')

		if currentID + 1 != len(probList):
			with col2: nextButton = st.button('Next Problem')

		while True:
			if prevButton:
				clear_session_variables()
				next_id = st.session_state['prob_num'] - 1
				st.session_state['prob_num'] = next_id
				switch_page(probList[next_id]['fname'])

			if nextButton:
				clear_session_variables()
				next_id = st.session_state['prob_num'] + 1
				st.session_state['prob_num'] = next_id
				switch_page(probList[next_id]['fname'])

			if tryAgain:
				clear_session_variables()
				switch_page('problem_set_login')
				#switch_page(st.session_state['starting_page_name'])

			if exitButton:
				clear_session_variables()
				switch_page(st.session_state['course_problem_page'])

			time.sleep(1)
	else:
		ph = st.empty()

		#st.write(st.session_state['current_sec'])
		if 'score' in st.session_state:
			if st.session_state['score'] < 50: n_sec = n_sec*3
			elif st.session_state['score'] < 70: n_sec = n_sec*3
			elif st.session_state['score'] < 80: n_sec = n_sec*3
			elif st.session_state['score'] < 90: n_sec = n_sec*2
			elif st.session_state['score'] < 94: n_sec = n_sec*1
			elif st.session_state['score'] < 97: n_sec = int(n_sec*0.9)
			else: n_sec = int(n_sec*0.8)

		mm, ss = n_sec//60, n_sec%60
		exitButton = st.button('exit problems')

		[solution, response, sessionVar] = display_code()

		clicked = st.button('Submit')
		correct = False
		secs = 40
		for secs in range(n_sec,0,-1):
			st.session_state['current_sec'] = secs
			mm, ss = secs//60, secs%60
			ph.metric("Countdown", f"{mm:02d}:{ss:02d}")

			if exitButton:
				del st.session_state['current_sec']
				clear_session_variables()
				switch_page(st.session_state['course_problem_page'])
			elif clicked:
				if type(response).__name__	 == 'str':
					if response.lower().strip() == solution.lower().strip(): correct = True
				else:
					try:
						if isclose(response, float(solution), abs_tol=2e-2): correct = True
					except:
						st.write('Error : the standard_problem_page function ran into an error')
						time.sleep(20)
						raise ValueError('Error : the standard_problem_page function ran into an error')

				probList[currentID]['response'] = str(response)
				probList[currentID]['correct'] = correct
				st.session_state['prob_name_list'] = probList


				if correct: st.session_state['num_correct'] = st.session_state['num_correct'] + 1
				clear_session_variables(sessionVar)

				break
			time.sleep(1)

		if secs < 2:	# time ran out
			probList[currentID]['response'] = str('')
			probList[currentID]['correct'] = False

		try: clear_session_variables(sessionVar)
		except: clear_session_variables()

		del st.session_state['current_sec']
		next_page()


def next_page():
	next_id = st.session_state['prob_num'] + 1
	probList = st.session_state['prob_name_list']
	st.session_state['prob_num'] = next_id

	if next_id >= len(probList):
		switch_page('prob_termination_page')
	else:
		#print(probList[next_id]['fname'])
		switch_page(probList[next_id]['fname'])


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

def input_field(label, inputType='text', columns=None, type="default", key=None):
	c1, c2 = st.columns(columns or [1, 4])

	# Display field name with some alignment
	c1.markdown("##")
	c1.markdown(label)


	if inputType == 'text' and key is None:
		raise ValueError('For input_field with text, you must provide a key')

	if key is None: v = gen_random_string(str_len=10)
	else: v = key
	add_page_specific_session_id(v)

	# Forward text input parameters
	if inputType == 'text':
		return c2.text_input(label='V', value='', type=type, label_visibility='hidden', key=v)
	else:
		return c2.number_input(label='V', label_visibility='hidden', value=0.0, key=v, min_value=-10000000.0, max_value=10000000.0, step=1e-4)

def variable_to_string_list(varList):
	newList = []
	for i in varList:
		if type(i).__name__ == 'list':
			newList.append(i)
		else:
			newList.append(str(i))

	return newList

def get_all_problems(n, fname):
	prob_base = []
	prob_list = []

	prob_name = (fname.split('_set_')[1])
	prob_name = prob_name.replace('.py','')
	all_pages = os.listdir('./pages')

	for p in all_pages:
		if p.find(prob_name) == 0:
			q = p.replace('.py','')
			prob_base.append({'fname':q})

	random.shuffle(prob_base)
	prob_list = prob_base[0:n]

	#for i in range(n):
	#	rV = random.randint(0,len(prob_base)-1)
	#	prob_list.append(prob_base[rV].copy())


	path, filen = os.path.split(fname)
	curFname = filen.replace('.py','')

	return curFname, prob_list

def wrong_user_type(usrType):
	if 'user_type' not in st.session_state:
		st.markdown(r''' ## Note that this is a web App, so refreshing the page erases all app memory 😉, and you need to sign in again ... ''')
		tryAgain = st.button('Login')
		while True:
			time.sleep(1)
			if tryAgain: switch_page('streamlit_app')
		return True

	if st.session_state['user_type'] < usrType:
		st.markdown(r''' ## Note that this is a web App, so refreshing the page erases all app memory 😉, and you need to sign in again... ''')
		tryAgain = st.button('Login')
		while True:
			time.sleep(1)
			if tryAgain: switch_page('streamlit_app')
		return True

	return False


def problem_display_ending(solution=None, answerType='text'):
	if 'page_global_variables' not in st.session_state:
		st.session_state['page_global_variables'] = []

	frame = inspect.stack()[1]
	module = inspect.getmodule(frame[0])
	key = module.__file__.strip('.py').split('/')[-1]

	probList = st.session_state['prob_name_list']
	currentID = st.session_state['prob_num']
	probList[currentID]['input'] = variable_to_string_list(st.session_state['page_global_variables'])

	probList[currentID]['solution'] = str(solution)
	response = input_field('Answer', inputType=answerType, key=key)

	params = [solution, response, [] ]
	return params



#	Previous version
#def problem_display_ending(varList=None, solution=None, sessionVar=[], answerType='text', key=None):
#	if 'page_global_variables' not in st.session_state:
#		st.session_state['page_global_variables'] = []
#
#	if key is None:	# automatically set the key value
#		frame = inspect.stack()[1]
#		module = inspect.getmodule(frame[0])
#		key = module.__file__.strip('.py').split('/')[-1]
#
#	probList = st.session_state['prob_name_list']
#	currentID = st.session_state['prob_num']
#
#	if varList is None or varList == []:		# this make it backward compatible for now, should eventually fix this
#		#print(st.session_state['page_global_variables'])
#		#print('\n\n------------------------\n\n')
#		probList[currentID]['input'] = variable_to_string_list(st.session_state['page_global_variables'])
#	else:
#		probList[currentID]['input'] = variable_to_string_list(varList)
#
#	probList[currentID]['solution'] = str(solution)
#	response = input_field('Answer', inputType=answerType, key=key)
#
#	params = [solution, response, sessionVar]
#	return params

def set_page_variables_for_display(var):
	st.session_state['page_global_variables'] = var

def retrieve_display_variables(correct=None):
	probList = st.session_state['prob_name_list']
	currentID = st.session_state['prob_num']

	if problem_has_been_answered():
		correct = probList[currentID]['correct']

	if correct is None:
		return st.session_state['page_global_variables']
	else:
		probList = st.session_state['prob_name_list']
		currentID = st.session_state['prob_num']
		return probList[currentID]['input']

def vector_to_norm(r, norm_type):
	if norm_type == 'maximum': solution = np.max(r)
	elif norm_type == 'minimum': solution = np.min(r)
	elif norm_type == 'total sum': solution = np.sum(r)
	elif norm_type == 'L1 norm': solution = np.linalg.norm(r, ord=1)
	elif norm_type == 'L2 norm squared': solution = np.linalg.norm(r, ord=2)*np.linalg.norm(r, ord=2)
	elif norm_type == 'L2 norm': solution = np.linalg.norm(r, ord=2)
	elif norm_type == 'infinity norm': solution = np.linalg.norm(r, ord=np.inf)
	elif norm_type == 'max(x)': solution = np.max(r)
	elif norm_type == 'min(x)': solution = np.min(r)
	elif norm_type == 'sum(x)': solution = np.sum(r)
	elif norm_type == '||x||_1': solution = np.linalg.norm(r, ord=1)
	elif norm_type == '||x||_2^2': solution = np.linalg.norm(r, ord=2)*np.linalg.norm(r, ord=2)
	elif norm_type == '||x||_2': solution = np.linalg.norm(r, ord=2)
	elif norm_type == '||x||_{\infty}': solution = np.linalg.norm(r, ord=np.inf)
	elif norm_type == 'Manhattan norm': solution = np.linalg.norm(r, ord=1)
	elif norm_type == 'Euclidean norm squared': solution = np.linalg.norm(r, ord=2)*np.linalg.norm(r, ord=2)
	elif norm_type == 'Euclidean norm': solution = np.linalg.norm(r, ord=2)
	elif norm_type == 'uniform norm': solution = np.linalg.norm(r, ord=np.inf)
	elif norm_type == 'maximum norm': solution = np.linalg.norm(r, ord=np.inf)
	elif norm_type == 'supremum norm': solution = np.linalg.norm(r, ord=np.inf)

	return solution
