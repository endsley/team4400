import streamlit as st
import numpy as np
import pandas as pd
from io import StringIO
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem(v1, L):
            display_color_problem_title() 

            # Display description and the table
            display_new_line(
                r'''Given the probability table below where $X$ represents the probability of you having a good or bad date and $Y$ represents the potential topics you could talk about during a date.''')
            st.write(v1)

            # Display specific question
            display_new_line(r'''What is the probability that you would talk about food and have a good date?''')

        # Check if the problem has already been answered
        if problem_has_been_answered():
            [v1, L] = retrieve_display_variables()
            v1 = pd.read_csv(StringIO(v1), header=0, index_col=0)
            display_problem(v1, L)
            params = display_solutions()
        else:
            # Generate random data
            dx = 2  # Dimensions for X (good, bad)
            dy = 4  # Dimensions for Y (ex, food, travel, weather)
            v1 = get_random_joint_distribution_table(x_dim=dx, y_dim=dy, sessionID='v1')
            v1 = v1.rename(columns={'x=0': 'x=good', 'x=1': 'x=bad'},
                           index={'y=0': 'y=ex', 'y=1': 'y=food', 'y=2': 'y=travel', 'y=3': 'y=weather'})
            L = 'food'  # Focus on 'food' topic

            # Define key variables and display the problem
            set_page_variables_for_display([v1.to_csv(), L])  # dataframe can only be transported as string
            display_problem(v1, L)

            # Define the solution
            P = v1.to_numpy() # Obtain the joint distribution table as a numpy array
            solution = np.round(P[1, 0], 2)  # Probability of 'food' and 'good'
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)
