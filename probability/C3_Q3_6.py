import streamlit as st
import numpy as np
from utils import *
from io import StringIO
import pandas as pd

if __name__ == "__main__":
    n_sec = 100


    def display():
        def display_problem():
            display_color_problem_title()

            [v1, L] = retrieve_display_variables()
            v1 = pd.read_csv(StringIO(v1), header=0, index_col=0)
            display_new_line(
                r'''Given the probability table below where $X$ represents the probability of you having a good or bad date and $Y$ represents the potential topics you could talk about during a date.''')
            st.write(v1)

            display_new_line(f'What is the probability you have a good date given you talk about the weather? Solve this problem {L} Round your answer to the nearest second decimal place.')

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # generate random data
            dx = 2
            dy = 4
            v1 = get_random_joint_distribution_table(x_dim=dx, y_dim=dy, sessionID='v1')
            v1 = v1.rename(columns={'x=0': 'x=good', 'x=1': 'x=bad'},
                           index={'y=0': 'y=ex', 'y=1': 'y=food', 'y=2': 'y=travel', 'y=3': 'y=weather'})

            v2 = getInt(0, 1, sessionID='v2')

            L = ['with conditional probability.', 'using Bayes rule.'][v2]

            # define key variables and display the problem
            set_page_variables_for_display([v1.to_csv(), L])  # dataframe can only be transported as string
            display_problem()

            # define the solution
            solution = np.round(v1.iloc[3]['x=good']/v1.loc['y=weather'].sum(), 2)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params


    standard_problem_page(n_sec, display)
