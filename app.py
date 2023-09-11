
import streamlit as st
import logging
import os

from annotated_text import annotation
from json import JSONDecodeError
from markdown import markdown
from utils.config import parser
from utils.haystack import start_document_store, start_haystack_extractive, start_haystack_rag, query
from utils.ui import reset_results, set_initial_state

try:
    args = parser.parse_args()
    document_store = start_document_store(type = args.store)
    if args.task == 'extractive':
        pipeline = start_haystack_extractive(document_store)
    else:
        pipeline = start_haystack_rag(document_store)

    set_initial_state()

    st.write('# '+args.name)

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
                st.session_state.results = query(pipeline, question)
            except JSONDecodeError as je:
                st.error(
                    "👓 &nbsp;&nbsp; An error occurred reading the results. Is the document store working?"
                )    
            except Exception as e:
                logging.exception(e)
                st.error("🐞 &nbsp;&nbsp; An error occurred during the request.")
            
                

    if st.session_state.results:
        results = st.session_state.results
        
        if args.task == 'extractive':
            answers = results['answers']
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
        elif args.task == 'rag':
            st.write(results['results'][0])
except SystemExit as e:
    # This exception will be raised if --help or invalid command line arguments
    # are used. Currently streamlit prevents the program from exiting normally
    # so we have to do a hard exit.
    os._exit(e.code)