#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 06:54:16 2023

@author: tingtingzhao
"""

#!/usr/bin/env python

import streamlit as st
from utils import *
import numpy as np
from math import isclose
import pandas as pd
from PIL import Image
import time

if __name__ == "__main__":
    n_sec = 50
    
    def display():
        #	Define this function for new proble
        def display_problem():
            display_color_problem_title()
            #	parts where you change
            [v1] = retrieve_display_variables()
            display_new_line(r'''8.	Do heavier cars use more gasoline? To answer this question, a researcher randomly selected 15 cars. He collected their weight (in hundreds of pounds) and the mileage (MPG) for each car. From a scatterplot made with the data, a linear model seemed appropriate. Which of the following descriptions of the value of the slope is the correct description?''')
            image = Image.open('./pages/images/coeff.png')
            st.image(image, caption='Coefficients summary table')
            
            display_multiple_choice(v1)


		# -------------------------------------------------------------------
        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
			#	randomize multiple choice
			#v1 = multiple_choice([	'joint distribution', 	# first one is always the answer
			#						'multi-distribution',	# the code will automatically randomize for you
			#						'poly-distribution' ], 'v1')	# Very import to include the session id for variable used
            v1 = multiple_choice(['We estimate the mileage to decrease by 0.521 miles per gallon when the weight of a car increases by 100 pounds.',
                                  'We estimate the mileage to decrease by 52.1 miles per gallon when the weight of a car increases by 100 pounds.',
                                  'We estimate the mileage to decrease by 0.521 miles per gallon when the weight of a car increases by 1 pound.',
                                  'We cannot interpret the slope because we cannot have a negative weight of a car.'], 'v1')
            set_page_variables_for_display([v1])
            display_problem()
            # define the solution	
            solution = v1[0]
			params = problem_display_ending(solution, 'text')
            return params
    standard_problem_page(n_sec, display)
    
    
