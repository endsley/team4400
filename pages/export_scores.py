import streamlit as st
from streamlit_extras.switch_page_button import switch_page
problem_set = st.session_state['problem']
st.write("## Scores of", problem_set)
back = st.button('Back')
if back:
    switch_page('teacher_course_page')
student_list = st.session_state['student_list']
scores = st.session_state['scores']
t1, t2 = st.columns([2, 2])
with t1:
    st.write('**:blue[Name]**')
with t2:
    st.write('**:blue[Score]**')
col1, col2 = st.columns([2, 2])
for i in range(len(student_list)):
    with col1:
        st.write(student_list[i])
    with col2:
        st.write(scores[i])