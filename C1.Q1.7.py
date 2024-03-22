import streamlit as st
from utils import *

if __name__ == "__main__":
    n_sec = 100

    def display():
        def display_problem():
            display_color_problem_title()
            [random1_val1, random1_val2, random1_val3, random2_val1, random2_val2, random3_val3] = retrieve_display_variables()
            display_new_line(r''' Given \\ 
\begin{equation*}
  x = \begin{bmatrix}
    %d \\
    %d\\
    %d
\end{bmatrix},   
  y = \begin{bmatrix}
    %d \\
    %d \\
    %d
\end{bmatrix},   
\end{equation*}
Calculate the following: $\langle y, x \rangle$''', 
                             (random1_val1, random1_val2, random1_val3, random2_val1, random2_val2, random3_val3))


        if problem_has_been_answered():
            display_problem()
            params = display_solutions()
        else:
            [random1_val1, random1_val2, random1_val3, random2_val1, random2_val2, random3_val3] = getMultInts(6, 1, 3)
            set_page_variables_for_display([random_addon, random_coefficient, power, random_lower, random_upper])
            display_problem()
            def anti_derivative(x):
                return random_coefficient * (1 / (power + 1)) * x**(power + 1) + random_addon*x
            def solve_anti_deriv():
                return anti_derivative(random_upper) - anti_derivative(random_lower)
            solution = solve_anti_deriv()
            params = problem_display_ending(solution, 'number')

            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write("Solution is: " + str(solution))

        return params

    standard_problem_page(n_sec, display)

