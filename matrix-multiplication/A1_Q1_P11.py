import streamlit as st
import numpy as np
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()

            [a,b,c,d,e,f] = retrieve_display_variables()
            display_new_line(r'''Z =  $$\begin{bmatrix} %d & %d & %d  \\ %d & %d & %d  \end{bmatrix}$$ ''',(a, b, c, d, e, f))
            display_new_line(r''' What is $$Tr(Z^TZ)$$ ?''')


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # generate random data
            [a,b,c,d,e,f] = getMultInts(6, -3, 3)

			# define key variables and display the problem
            set_page_variables_for_display([a, b, c, d, e, f])
            display_problem()

			# define the solution	
            z = np.array([[a, b, c], [d, e, f]])
            solution = np.trace(z.T.dot(z))
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

