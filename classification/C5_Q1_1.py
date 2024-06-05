import streamlit as st
import numpy as np
from utils import *
from io import StringIO
import pandas as pd

if __name__ == "__main__":
    n_sec = 180


    def display():
        def display_problem():
            display_color_problem_title()

            [v1] = retrieve_display_variables()
            v1 = pd.read_csv(StringIO(v1), header=0, index_col=0)
            display_new_line(
                r'''Given the probability table below where $X$ represents the probability of you having a good or bad date and $Y$ represents the potential topics you could talk about during a date.''')
            st.write(v1)

            display_new_line(r'''Calculate the mutual information $I(X, Y)$''')

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            # generate random data
            dx = 2
            dy = 2
            v1 = get_random_joint_distribution_table(x_dim=dx, y_dim=dy, sessionID='v1')
            v1 = v1.rename(columns={'x=0': 'x=good', 'x=1': 'x=bad'},
                           index={'y=0': 'y=ex', 'y=1': 'y=food'})


            # define key variables and display the problem
            set_page_variables_for_display([v1.to_csv()])  # dataframe can only be transported as string
            display_problem()

            # Define the solution
            solution = np.round(
                (v1.iloc[0]['x=good'] * np.log2(v1.iloc[0]['x=good'] / (v1['x=good'].sum() * v1.loc['y=ex'].sum()))) +
                (v1.iloc[0]['x=bad'] * np.log2(v1.iloc[0]['x=bad'] / (v1['x=bad'].sum() * v1.loc['y=ex'].sum()))) +
                (v1.iloc[0]['x=good'] * np.log2(v1.iloc[0]['x=good'] / (v1['x=good'].sum() * v1.loc['y=food'].sum()))) +
                (v1.iloc[0]['x=bad'] * np.log2(v1.iloc[0]['x=bad'] / (v1['x=bad'].sum() * v1.loc['y=food'].sum())))
                , 2)

            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params


    standard_problem_page(n_sec, display)
