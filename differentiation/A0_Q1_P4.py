import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 180

    def display():
        def display_problem():
            display_color_problem_title()
            [random_coefficient, random_x, random_y_1, random_y_2, random_y_3] = retrieve_display_variables()
            display_new_line(r'''Given the function $f(x)=\sum_{i=1}^{3}\left (%d x - y_i  \right )^2$''', (random_coefficient))
            display_new_line(r'''where $y = \begin{bmatrix} %d\\ %d\\ %d \end{bmatrix}$''', (random_y_1, random_y_2, random_y_3))
            display_new_line(r'''Evaluate the derivative of $f(x)$ when $x = %d $''', (random_x))

        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            [random_coefficient, random_x, random_y_1, random_y_2, random_y_3] = getMultInts(5, 2, 5)
            set_page_variables_for_display([random_coefficient, random_x, random_y_1, random_y_2, random_y_3])
            display_problem()
            def derivative(x):
                sum = 0
                sum += random_coefficient * (random_coefficient * x - random_y_1)
                sum += random_coefficient * (random_coefficient * x - random_y_2)
                sum += random_coefficient * (random_coefficient * x - random_y_3)
                sum = 2 * sum
                return sum

            solution = derivative(random_x)
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)
