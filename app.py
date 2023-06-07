
from annotated_text import annotation
from json import JSONDecodeError
import logging
from markdown import markdown

import streamlit as st

from utils.haystack import query
from utils.ui import reset_results, set_initial_state

set_initial_state()

st.write("# Srart building out the content of your application here")

# Search bar
question = st.text_input("Ask a question", value=st.session_state.question, max_chars=100, on_change=reset_results)

run_pressed = st.button("Run")

run_query = (
    run_pressed or question != st.session_state.question
)

# Get results for query
if run_query and question:
    reset_results()
    st.session_state.question = question
    with st.spinner("🔎 &nbsp;&nbsp; Running your pipeline"):
        try:
            st.session_state.results = query(question)
        except JSONDecodeError as je:
            st.error(
                "👓 &nbsp;&nbsp; An error occurred reading the results. Is the document store working?"
            )    
        except Exception as e:
            logging.exception(e)
            st.error("🐞 &nbsp;&nbsp; An error occurred during the request.")
        
            

if st.session_state.results:
    st.write('## Do something with your results')
    answers = st.session_state.results
    
    for count, answer in enumerate(answers):
        if answer.answer:
            text, context = answer.answer, answer.context
            start_idx = context.find(text)
            end_idx = start_idx + len(text)
            st.write(
                markdown(context[:start_idx] + str(annotation(body=text, label="ANSWER", background="#964448", color='#ffffff')) + context[end_idx:]),
                unsafe_allow_html=True,
            )
        else:
            st.info(
                "🤔 &nbsp;&nbsp; Haystack is unsure whether any of the documents contain an answer to your question. Try to reformulate it!"
            )