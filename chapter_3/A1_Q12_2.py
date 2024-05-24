import numpy as np
import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 600

    def display():
        def display_problem():
            display_color_problem_title()
            [num1,num2,num3,num4,num5] = retrieve_display_variables()
            display_new_line(
                r'''
                Given the following probability table:
                
                $
                \\
                p(x = %d) = %.1f\\
                p(x = %d) = %.1f\\
                p(x = %d) = %.1f\\
                $
                ''',
                (num1,num4*0.1,num2,num4*0.1,num3,num5*0.1)
            )
            display_new_line(
                r''' 
               What is population Var[x]?
                '''
            )
            
        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # get values for matrix and display
            mat_vals = getMultInts(5, 1, 9)
            [num1,num2,num3,num4,num5] = mat_vals
            set_page_variables_for_display([num1,num2,num3,num4,num5])
            display_problem()
            
            # def sample_exp function
            def variance(num1,num2,num3,num4,num5):
                mean = num1*num4*0.1 + num2*num4*0.1+num3*num5*0.1
                var = ((num1 - mean)**2)*num4*0.1+((num2-mean)**2)*num4*0.1+((num3-mean)**2)*num5*0.1
                return var 
            
            # calculate the estimated solution
            solution = variance(num1,num2,num3,num4,num5)

            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

