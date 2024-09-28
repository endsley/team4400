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
from math import isclose, e
import numpy as np
import pandas as pd
from deta import Deta
from copy import deepcopy
from sklearn.preprocessing import normalize
from sympy import *
import sympy as sp
from sympy import simplify, parse_expr, N
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
import ast
import random
from tokenize import TokenError
#from streamlit_js_eval import get_page_location
import re
from fractions import Fraction
#from pathlib import Path
from streamlit.source_util import (
    page_icon_and_name,
    calc_md5,
    get_pages,
    _on_pages_changed
)

from sympy import Symbol, sympify, parse_expr
from sympy.core.sympify import SympifyError
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application

# define some global variables
transformations = (standard_transformations + (implicit_multiplication_application,))

# Define custom local dictionary for parse_expr
local_dict = {'log': sp.log,
              'e': e}
replacements = {'E': 'e'}


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
    if 'is_practice_exam_review' in st.session_state.keys() and st.session_state['is_practice_exam_review']:  # Logic changes when we are working with the practice exams
        current_exam = st.session_state['starting_page_name']
        deta = Deta(st.secrets["data_key"])
        db = deta.Base("hw_test_results")

        quiz_results = db.fetch(
            {'account_key': st.session_state['student_key'], "practice_exam": current_exam}).items

        if 'latest_result_package' in list(quiz_results[0].keys()):
            probList = quiz_results[0]['latest_result_package']
            st.session_state['prob_name_list'] = probList
    else:
        probList = st.session_state['prob_name_list']

    currentID = st.session_state['prob_num']

    if 'correct' in probList[currentID]:
        return True
    else:
        return False


def display_solutions(additional_display=None):
    is_exam = st.session_state.get('is_exam')

    currentID = st.session_state['prob_num']

    probList = st.session_state['prob_name_list']
    solution = probList[currentID]['solution']
    response = probList[currentID]['response']
    if is_exam: # Dont want students to see the correct answer mid-exam
        if response == '' or response is None: response = '(did not provide a response)'
        st.code('Your response is %s' % response, language='python')

    else:
        if response == '' or response is None: response = '(did not provide a response)'
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
            line = line.replace('%.1f','%s')
            line = line.replace('%.2f','%s')
            line = line.replace('%.3f','%s')
            line = line.replace('%.4f','%s')
            st.markdown(line%variables)

def display_color_problem_title(correct=None, prob_id=None, numProbs=None):
    is_exam = st.session_state.get('is_exam')

    probList = st.session_state['prob_name_list']
    currentID = st.session_state['prob_num']

    if problem_has_been_answered():
        correct = probList[currentID]['correct']

    if numProbs is None:
        numProbs = len(probList)
        prob_id = st.session_state['prob_num'] + 1

    if is_exam:
        # For practice exams, show a simplified or different format
        st.markdown(r'''## Question %d''' % prob_id)

    else:
        # For homework and practice exam review, use the existing format
        if correct:
            st.markdown(r'''### :green[Problem %d out of %d is Correct]''' % (prob_id, numProbs))
        elif correct is None:
            st.markdown(r'''## Problem %d out of %d''' % (prob_id, numProbs))
        else:
            st.markdown(r'''### :red[Problem %d out of %d is Incorrect]''' % (prob_id, numProbs))

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


def get_random_joint_distribution_table(x_dim=2, y_dim=3, non_zero=True, sessionID=None):
    if sessionID is not None:
        if sessionID in st.session_state:
            return st.session_state[sessionID]
    while True: # Continue to generate new X and Y values until none of them are 0 or negative
        Y = np.round(np.random.rand(1, x_dim),1)
        Y = np.round(Y/np.sum(Y), 2)
        err = 1 - np.sum(Y)
        Y[0] = Y[0] + err

        # Check for zero values in Y if non_zero is True
        if non_zero and (np.any(Y == 0) or np.any(Y < 0)):
            continue


        X = np.round(np.random.rand(y_dim, x_dim),1)
        X = np.round(normalize(X, axis=0, norm='l1'),2)
        d = np.array([1,1]) - np.sum(X,axis=0)
        X[0,:] = X[0,:] + d

        if non_zero and (np.any(Y == 0) or np.any(Y < 0)):
            continue

        break

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




def get_rand(minV,maxV, sessionID=None, rounding=1):
    if sessionID is not None:
        if sessionID in st.session_state:
            return st.session_state[sessionID]

    random.seed()
    outV = (maxV - minV)*np.random.rand() + minV
    outV = np.round(outV, rounding)

    if sessionID is not None:
        st.session_state[sessionID] = outV
        add_page_specific_session_id(sessionID)
    return outV



def getInt(minV,maxV, sessionID=None, decimal=False):
    if sessionID is not None:
        if sessionID in st.session_state:
            return st.session_state[sessionID]

    random.seed()
    outV = random.randint(minV,maxV)
    if decimal:
        outV = outV/10
    if sessionID is not None:
        st.session_state[sessionID] = outV
        add_page_specific_session_id(sessionID)
    return outV


def getMultInts(n, minV, maxV, unique=False):
    if unique and (maxV - minV + 1) < n:
        raise ValueError("Range is too small to generate the requested number of unique integers")

    if unique:
        var = set()
    else:
        var = []

    while len(var) < n:
        sessionKey = 'v' + str(len(var) + 1)
        outV = getInt(minV, maxV, sessionID=sessionKey)

        if unique:
            var.add(outV)
        else:
            var.append(outV)

        add_page_specific_session_id(sessionKey)

    return list(var) if unique else var
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

	if probList[currentID]['fname'] != key:
		st.markdown(r''' ## Error: This is a web app, you cannot press the back button. Please log in again.''')
		st.stop()
def identify_response_type(response):
    """
    Evaluate what type of response the student gave.
    Options:
    - pure string, like in multiple choice questions.
    - string, but as a mathematical expression.
    - numerical value.
    - string, but as a list (either a list of tuples or a list of lists, or just a 1D list)
    - string, as a tuple
    """

    def contains_np(obj):
        if isinstance(obj, str):
            return 'np' in obj
        elif isinstance(obj, list):
            return any(contains_np(item) for item in obj)
        return False

    if contains_np(response):
        return 'text'

    # Check if the response is a list of lists or tuples
    try:
        parsed_response = eval(response)
        if isinstance(parsed_response, list):
            return 'list'
        elif isinstance(parsed_response, tuple):
            return 'tuple'
    except (ValueError, SyntaxError, TypeError, NameError):
        pass

    try:
        # Attempt to parse the response as a mathematical expression
        parsed_expr = parse_expr(response, transformations=transformations)

        # Check if the parsed expression is valid
        if isinstance(parsed_expr, (int, float)):
            return 'number'
        else:
            return 'math_expression'
    except (SyntaxError, TypeError, TokenError, AttributeError):
        try:
            # Attempt to convert the response to a numerical value
            float(response)
            return 'number'
        except ValueError:
            try:
                # Attempt to sympify the response to check for mathematical expressions
                sympified_expr = sympify(response)
                if isinstance(sympified_expr, (int, float)):
                    return 'number'
                else:
                    return 'math_expression'
            except SympifyError:
                return 'text'


def convert_string_to_float_elements(response):
    """
    Converts a string of
        1) A list
        2) A list of lists
        3) A list of tuples
    To a list with simplified values

    Example:
        - '[(9/2, -1/2), (-5/3, 4)]' evaluates to [(4.5, -0.5), (-1.6666666666666667, 4)]
        - '[[9/2, -1/2], [-5/3, 4]]' evaluates to [[4.5, -0.5], [-1.6666666666666667, 4]]
        - '[sqrt(4) + 3/4 + e**0, (4/5) + 5]' evaluates to [3.75, 5.8]
        - '[(sqrt(4) + 3/4, -1/2), (e**0, 4)]' evaluates to [(3.75, -0.5), (1.0, 4)]

    """

    def evaluate_expression(expression):
        """Evaluates and simplifies mathematical expressions using sympy."""
        return float(sp.sympify(expression))

    def parse_structure(text):
        """Recursively parse and evaluate expressions, handling nested lists and tuples."""
        if text.startswith('[') and text.endswith(']'):
            # Handle list of expressions
            text = text[1:-1]  # Strip outer brackets
            items = split_items(text)
            return [parse_structure(item.strip()) for item in items]

        elif text.startswith('(') and text.endswith(')'):
            # Handle tuple of expressions
            text = text[1:-1]  # Strip outer parentheses
            items = split_items(text)
            return tuple(parse_structure(item.strip()) for item in items)

        else:
            # Evaluate the expression
            return evaluate_expression(text)

    def split_items(text):
        """Splits items considering nested structures."""
        items = []
        brackets = 0
        current_item = []

        for char in text:
            if char in '[(':
                brackets += 1
            elif char in '])':
                brackets -= 1

            if char == ',' and brackets == 0:
                items.append(''.join(current_item).strip())
                current_item = []
            else:
                current_item.append(char)

        if current_item:
            items.append(''.join(current_item).strip())

        return items

    # Parse the input and evaluate
    return parse_structure(response)



def convert_fractions_string(fractions_str):
    """
    Convert a string containing Fraction objects to a string with fractions in 'a/b' format,
    maintaining the original matrix structure with commas.

    Parameters:
    - fractions_str (str): The input string containing Fraction objects.

    Returns:
    - str: The converted string with fractions in 'a/b' format and commas.
    """

    # Define a function to convert Fraction to 'a/b' format or whole number if denominator is 1
    def fraction_to_str(match):
        # Extract the numerator and denominator from the match
        fraction = eval(match.group())
        if fraction.denominator == 1:
            return f"{fraction.numerator}"
        return f"{fraction.numerator}/{fraction.denominator}"

    # Regular expression to match 'Fraction(a, b)' patterns
    pattern = re.compile(r'Fraction\((\-?\d+),\s*(\d+)\)')

    # Replace all occurrences of 'Fraction(a, b)' with 'a/b' or just 'a' if denominator is 1
    result = pattern.sub(fraction_to_str, fractions_str)

    # Maintain matrix formatting by replacing spaces around brackets with commas
    result = result.replace(' ', ', ')
    result = result.replace(',\n', '], [')
    result = result.replace('[', '[[').replace(']', ']]')

    return result


def clean_solution_string(solution_str):
    """
    Cleans the solution string by removing newline characters and unnecessary commas.
    """
    # Remove newline characters
    solution_str = solution_str.replace('\n', '').replace('[, ', '[').replace(',]', ']')

    # Remove unnecessary commas
    solution_str = re.sub(r',\s*,', ',', solution_str)

    # Clean up extra brackets that might result from the conversion
    solution_str = re.sub(r'\[\[\s*', '[', solution_str)
    solution_str = re.sub(r'\s*\]\]', ']', solution_str)

    return solution_str


def standardize_expression(expr_str, replacements):
    """
    Standardizes the expression by replacing keys in the replacements dictionary.
    """
    for key, value in replacements.items():
        expr_str = expr_str.replace(key, str(value))
    return expr_str


def compare_response(response, solution):
    """
    Checks if the student's answer is correct.
    """
    if response is None or response == 'No Response': # If a student doesn't answer
        return False

    response_type = identify_response_type(response)

    if response_type == 'number':
        try:
            # Convert response to float for comparison
            response = float(response)
            # Evaluate the solution if it's a string representing a math expression
            if isinstance(solution, str):
                solution = float(parse_expr(solution).evalf())
            return isclose(response, solution, abs_tol=2e-2)
        except (ValueError, TypeError, SympifyError):
            return False

    elif response_type == 'math_expression':
        try:
            # Standardize the response and solution
            response = standardize_expression(response, replacements)

            # Attempt to simplify the response as an expression
            parsed_expr = parse_expr(response)
            response_value = simplify(parsed_expr)
            if isinstance(solution, str):  # Most times the solution will be a string as it is a math expression as well
                solution = standardize_expression(solution, replacements)
                parsed_sol = parse_expr(solution)
                solution_value = simplify(parsed_sol)

            else:
                solution_value = simplify(solution)

            return response_value == solution_value
        except (SyntaxError, TokenError, ValueError):
            return False


    elif response_type == 'text':
        def normalize_spacing(expr):
            return expr.replace(" ", "")  # Want student answers to still be counted as correct even if the spacing is off

        normalized_response = normalize_spacing(response)
        if isinstance(solution, list):  # If there are multiple solution options
            for sol in solution:  # Multiple solution options
                normalized_solution = normalize_spacing(sol)
                # Compare the normalized response with the normalized solution
                if normalized_response == normalized_solution:
                    return True
        # Compare as strings
        return response.strip().lower() == solution.strip().lower()

    elif response_type == 'list':
        try:
            response_list = convert_string_to_float_elements(response)  # Simplify the student's answer
            if isinstance(solution, str):  # This will be used for matrix questions
                solution = clean_solution_string(solution)  # Clean up any unnecessary characters
                solution = eval(solution)
            return sorted(response_list) == sorted(solution)
        except (ValueError, SyntaxError):
            return False

    elif response_type == 'tuple':
        try:
            # Convert the string to a tuple of sympy expressions
            expression = eval(response.replace('sqrt', 'sp.sqrt'))
            # Evaluate the expression
            result = tuple(sp.N(sp.sympify(expr)) for expr in expression)
            # Convert solution to a tuple if it is not already one
            if not isinstance(solution, tuple):
                solution = tuple(solution)
            return result == solution
        except (ValueError, SyntaxError):
            return False

    else:
        return False


def standard_problem_page(n_sec, display_code):
    """
    This function is organized in the following way:

    if correct in probList[currentID] (reviewing an answer):
        if not actively taking an exam:
            if in the exam review page:
                ...
            if in the homework review page:
                ...
        if actively taking an exam:
            ... (This logic allows students to review their answers while they are taking an exam to check before submitting)

    else: (They are not reviewing their answers, they are either actively doing the homework or an exam)
        if actively taking an exam:
            in the exam, students have the option to go to previous problem or next problem.

        if doing homework:
            only has the option to press "submit" which automatically take you to the next problem (maybe change this one day?)

    """
    page_properly_initialized(1, title="Problem set", icon="❓")
    problem_set_page_properly_initialized()

    # Reserve space for the error message at the top
    error_placeholder = st.empty()

    if 'current_sec' in st.session_state:
        n_sec = st.session_state['current_sec']

    probList = st.session_state['prob_name_list']
    currentID = st.session_state['prob_num']

    is_exam = st.session_state.get('is_exam', False)
    is_practice_exam_review = st.session_state.get('is_exam_review', False)

    if 'correct' in probList[currentID]: # Reviewing
        colA, colB = st.columns([1, 1])
        prevButton = False
        nextButton = False

        if not is_exam: # Need a separate chunk of code for non-exam review because they don't need the timer
            if is_practice_exam_review: # What goes above the question
                with colA:
                    if is_practice_exam_review:
                        return_to_review = st.button('Return to Review Page')
                if return_to_review:
                    clear_session_variables()
                    switch_page('practice_exam_review_page')
            else: # Homework
                with colA:
                    tryAgain = st.button('Try Again')
                with colB:
                    exitButton = st.button('Exit')
                if tryAgain:
                    clear_session_variables()
                    switch_page('problem_set_login')
                if exitButton:
                    clear_session_variables()
                    switch_page(st.session_state['course_problem_page'])

            params = display_code()

            col1, col2 = st.columns([1, 1])
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

                time.sleep(1)

        elif is_exam: # Need separate logic because of timer
            ph = st.empty()
            number_of_times = 0
            for secs in range(n_sec, 0, -1):
                st.session_state['current_sec'] = secs
                mm, ss = secs // 60, secs % 60
                ph.metric("Time left in exam", f"{mm:02d}:{ss:02d}")

                # Initialize the buttons outside the loop
                tryAgain = None
                exitButton = None
                prevButton = None
                nextButton = None

                if number_of_times == 0:  # don't make duplicate buttons
                    with colA:
                        tryAgain = st.button('Try Again', key=f"try_again_exam_{currentID}_{secs}")
                    with colB:
                        exitButton = st.button('Return to Exam Page', key=f"exit_exam_{currentID}_{secs}")

                    params = display_code()
                    col1, col2 = st.columns([1, 1])
                    if currentID != 0:
                        with col1:
                            prevButton = st.button('Previous Problem')

                    if currentID + 1 != len(probList):
                        with col2:
                            nextButton = st.button('Next Problem')

                # Handle button logic in a loop or conditionally outside
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

                # Additional conditions outside the number_of_times check
                if tryAgain:
                    # Clear response and correct status to allow reattempt
                    probList[currentID].pop('response', None)
                    probList[currentID].pop('correct', None)
                    st.session_state['prob_name_list'] = probList
                    st.session_state['prob_num'] = currentID  # Stay on the same problem
                    switch_page(probList[currentID]['fname'])

                if exitButton:
                    clear_session_variables()
                    switch_page('practice_exam')

                number_of_times += 1
                time.sleep(1)
    else:

        ph = st.empty()

        if not is_exam:
            exitButton = st.button('exit problems')
        else:
            exitButton = st.button('Return to Questions')

        [solution, response, sessionVar] = display_code()

        if isinstance(response, str):  # Avoid errors if a student doesn't give a response
            if response.strip() == "":
                response = str('No Response')

        clicked = st.button('Submit')

        correct = False

        secs = 40
        for secs in range(n_sec, 0, -1):
            st.session_state['current_sec'] = secs
            mm, ss = secs // 60, secs % 60
            ph.metric("Countdown", f"{mm:02d}:{ss:02d}")

            if exitButton:
                if not is_exam:
                    clear_session_variables()
                    del st.session_state['current_sec']
                    switch_page(st.session_state['course_problem_page'])
                else:
                    switch_page('practice_exam')
            elif clicked:
                try:
                    correct = compare_response(response, solution)
                    probList[currentID]['response'] = str(response)
                    probList[currentID]['correct'] = correct
                    st.session_state['prob_name_list'] = probList

                except (SyntaxError, TokenError, ValueError, TypeError, AttributeError):
                    error_placeholder.markdown(
                        '<p style="color:red; font-size:24px; font-weight:bold;">Invalid Response. Please try again</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        '<p style="color:red; font-size:24px; font-weight:bold;">Invalid Response. Please try again</p>',
                        unsafe_allow_html=True
                    )
                    time.sleep(10)
                if not is_exam:
                    if correct:
                        st.session_state['num_correct'] = st.session_state['num_correct'] + 1
                    clear_session_variables(sessionVar)
                break

            time.sleep(1)

        if not is_exam:
            if secs < 2:  # time ran out
                probList[currentID]['response'] = str('No response')
                probList[currentID]['correct'] = False
            try:
                clear_session_variables(sessionVar)
            except:
                clear_session_variables()
            del st.session_state['current_sec']

        next_page()  # This should only be called if not in exam mode


def next_page():
    is_exam = st.session_state.get('is_exam', False)
    next_id = st.session_state['prob_num'] + 1
    probList = st.session_state['prob_name_list']
    st.session_state['prob_num'] = next_id

    if next_id >= len(probList):
        if is_exam:
            switch_page('practice_exam')
        else:
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
    if inputType == 'text' or inputType == 'math_expression':
        return c2.text_input(label='V', value='', type=type, label_visibility='hidden', key=v)
    else:
        return c2.number_input(label='V', label_visibility='hidden', value=None, key=v, min_value=-10000000.0, max_value=10000000.0, step=1e-4)

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
def get_all_problem_files_for_exam(exam_name, modules_and_counts):
    """
    Grabs files from relevant modules for practice exams/exams

    Args:
        exam_name (str): Name of exam.
            - Example: practice_exam_1
        modules_and_counts (dict): Key is the module name, value is # of files you want from that module.
            - Example:
                modules_and_counts =
                {'differentiation': 3,
                 'integration': 2,
                 'matrix addition': 1}
    """
    exam_files = []
    for module, num_files in modules_and_counts.items():
        # Get all files for the module
        module_files = [f for f in os.listdir('pages') if f.startswith(module + '_')]

        if len(module_files) < num_files:
            raise ValueError(f"Not enough files in {module} module to select {num_files} files.")

        # Select random files from the module
        selected_files = random.sample(module_files, num_files)

        # Convert to the same format as probList for homework questions
        for file in selected_files:
            fname = file.replace('.py', '')
            exam_files.append({'fname': fname})

    return exam_name, exam_files

# TO DO: uncomment this when youre ready
# def get_all_problem_files_for_exam(exam_name, modules_and_counts, min_n_sec, max_n_sec, max_retries=10):
#     """
#     Grabs files from relevant modules for practice exams/exams and ensures total n_sec is within bounds.
#
#     Args:
#         exam_name (str): Name of exam.
#         modules_and_counts (dict): Key is the module name, value is # of files you want from that module.
#         min_n_sec (int): Minimum acceptable total n_sec.
#         max_n_sec (int): Maximum acceptable total n_sec.
#         max_retries (int): Maximum number of attempts to adjust file selection if total n_sec is out of bounds.
#     """
#     # Exam time based on the exam_name
#     if exam_name == 'practice_exam_final':
#         min_n_sec = 5700 # Can be done in between 95-105 minutes (but they are given 120 minutes)
#         max_n_sec = 6300
#     else:
#         min_n_sec = 4500  # Can be done in 75-85 minutes (but they are given 100 minutes)
#         max_n_sec = 5100
#         # Helper function to calculate total n_sec from selected files
#     def calculate_total_n_sec(selected_files):
#         total_n_sec = 0
#         for file in selected_files:
#             with open(os.path.join('pages', file), 'r') as f:
#                 content = f.read()
#             n_sec_match = re.search(r'n_sec\s*=\s*(\d+)', content)
#             if n_sec_match:
#                 n_sec = int(n_sec_match.group(1))
#                 total_n_sec += n_sec
#         return total_n_sec
#
#     retries = 0
#     max_retries = 10
#     while retries < max_retries:
#         exam_files = []
#         total_n_sec = 0
#
#         # Collect files for each module and calculate total n_sec
#         for module, num_files in modules_and_counts.items():
#             module_files = [f for f in os.listdir('pages') if f.startswith(module + '_')]
#
#             if len(module_files) < num_files:
#                 raise ValueError(f"Not enough files in {module} module to select {num_files} files.")
#
#             # Select random files from the module
#             selected_files = random.sample(module_files, num_files)
#
#             # Add the files to the final list
#             exam_files.extend(selected_files)
#
#         # Calculate the total n_sec for the selected files
#         total_n_sec = calculate_total_n_sec(exam_files)
#
#         # Check if total_n_sec is within the desired range
#         if min_n_sec <= total_n_sec <= max_n_sec:
#             break  # If within range, we are done
#         else:
#             retries += 1  # Retry if total_n_sec is out of bounds
#
#     if retries >= max_retries:
#         raise ValueError("Unable to select files with total n_sec within the specified range after multiple attempts.")
#
#     # Format the file names for the exam as per your original structure
#     exam_files_formatted = [{'fname': file.replace('.py', '')} for file in exam_files]
#
#     return exam_name, exam_files_formatted


def reset_exam_state():
    """
    Clears the session state for a fresh start to the exam.
    This function resets the problem list, answers, and checkmarks.
    """
    exam_name = st.session_state['starting_page_name']

    # Clear the current problem list, answers, and progress
    if f"pe_probList_{exam_name}" in st.session_state:
        del st.session_state[f"pe_probList_{exam_name}"]

    # Clear any stored filenames for problems
    if f"pe_curFname_{exam_name}" in st.session_state:
        del st.session_state[f"pe_curFname_{exam_name}"]

    # Clear the problem status and checkmarks
    if 'prob_name_list' in st.session_state:
        del st.session_state['prob_name_list']

    if 'prob_num' in st.session_state:
        del st.session_state['prob_num']

    if 'current_sec' in st.session_state:
        del st.session_state['current_sec']

    st.session_state['is_exam'] = False


def calculate_statistics(probList, n_sec):
    """
    Calculates the results of an exam and returns them in a structured format.
    """
    results = {
        'total_correct': sum(1 for result in probList if result.get('correct') is True),
        'total_questions': len(probList),
        'total_time': st.session_state['exam_time'] - n_sec # because n_sec is how much time they have left, so this is how much time it took them
    }

    score = 100 * results['total_correct'] / results['total_questions']
    attempt_time = results['total_time']

    # Create a result dictionary for each attempt
    return [score, attempt_time]
def update_practice_exam_results(exam_name, score, time_taken):
    """
    Updates the practice exam results for a student, appending new scores and times.

    Args:
    - exam_name (str): The name of the practice exam (e.g., 'practice_exam_1').
    - score (float): The student's score for the exam.
    - time_taken (float): The time it took the student to complete the exam.
    """

    # Initialize Deta Base
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("hw_test_results")

    # Fetch existing results for this student and exam
    student_key = st.session_state['student_key']
    results = db.fetch({'account_key': student_key, 'practice_exam': exam_name}).items

    if results:
        # If a record exists, retrieve it
        existing_record = results[0]
        current_scores = existing_record.get('practice_exam_score', [])
        current_times = existing_record.get('practice_exam_time', [])

        # Ensure the fields are lists (in case of a database schema mismatch)
        if not isinstance(current_scores, list):
            current_scores = [current_scores]
        if not isinstance(current_times, list):
            current_times = [current_times]

        # Append the new score and time to the respective lists
        current_scores.append(score)
        current_times.append(time_taken)

        # Update only the fields that need updating, including 'practice_exam'
        updates = {
            'practice_exam': exam_name,  # Ensure the practice_exam field is set
            'practice_exam_score': current_scores,
            'practice_exam_time': current_times
        }
        db.update(updates, existing_record['key'])

    else:
        # If no record exists, create a new one
        new_record = {
            'account_key': student_key,
            "account_name": st.session_state['user_name'],
            'practice_exam': exam_name,  # Set the practice_exam field
            'practice_exam_score': [score],
            'practice_exam_time': [time_taken]
        }
        print('Creating new record:', new_record)
        db.put(new_record)

def update_latest_result_package(exam_name):
    """
    Updates the 'latest_result_package' column for a student, overwriting it with the current list of problem names.

    Args:
    - exam_name (str): The name of the practice exam (e.g., 'practice_exam_1').
    """

    # Initialize Deta Base
    deta = Deta(st.secrets["data_key"])
    db = deta.Base("hw_test_results")

    # Fetch existing results for this student and exam
    student_key = st.session_state['student_key']
    results = db.fetch({'account_key': student_key, 'practice_exam': exam_name}).items

    if results:
        # If a record exists, retrieve it
        existing_record = results[0]

        # Update the record with the new 'latest_result_package'
        updates = {
            'practice_exam': exam_name,  # Ensure the practice_exam field is set
            'latest_result_package': st.session_state['prob_name_list']  # Overwrite the package
        }
        db.update(updates, existing_record['key'])

    else:
        # If no record exists, create a new one
        new_record = {
            'account_key': student_key,
            "account_name": st.session_state['user_name'],

            'practice_exam': exam_name,  # Set the practice_exam field
            'latest_result_package': st.session_state['prob_name_list']  # Set the initial package
        }
        print('Creating new latest results package:', new_record)
        db.put(new_record)


def display_exam_questions(question_files):
    st.write("### Questions")
    for i, q_file in enumerate(question_files):
        if st.button(f"Question {i + 1}", key=f"question_{i}"):
            st.session_state['current_question'] = q_file
            switch_page(q_file)  # Redirect to the question page


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


