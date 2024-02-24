from utils import *
import random

if __name__ == "__main__":
    n_sec = 100

    def display_integral_question():
        # Function to generate random coefficients, bounds, and power for the integral
        def generate_integral_parameters():
            c = random.randint(1, 5)  # Coefficient of x^n
            d = random.randint(0, 10)  # Constant term
            n = random.randint(2, 5)  # Power of x, can adjust range as needed
            a = 0  # Lower bound of the integral
            b = random.randint(1, 5)  # Upper bound of the integral
            return c, d, n, a, b

        def display_integral_problem(c, d, n, a, b):
            # Display the randomly generated integral problem
            display_new_line(f"Calculate the integral of $f(x) = {c}x^{n} + {d}$ over the interval $[{a}, {b}]$")

        def integral_solution(c, d, n, a, b):
            # Calculate the solution to the integral
            integral_c = (c / (n + 1)) * (b ** (n + 1) - a ** (n + 1))  # Integral of cx^n over [a, b]
            integral_d = d * (b - a)  # Integral of d over [a, b]
            return integral_c + integral_d

        c, d, n, a, b = generate_integral_parameters()  # Generate random problem parameters

        if problem_has_been_answered():
            display_integral_problem(c, d, n, a, b)
            params = display_solutions()  # Display solutions if the problem is answered
        else:
            display_integral_problem(c, d, n, a, b)
            solution = integral_solution(c, d, n, a, b)
            params = problem_display_ending(solution, 'number')

            # Preview mode for checking the solution before submission
            if 'preview' in st.session_state and st.session_state['preview'] == 1:
                st.write(f"Solution is: {solution}")

        return params

    standard_problem_page(n_sec, display_integral_question)
