import streamlit as st

from haystack import Pipeline
from haystack.schema import Answer
#Use this file to set up your Haystack pipeline and querying


# cached to make index and models load only at start
@st.cache_resource(show_spinner=False)
def start_haystack():
    #Use this function to contruct a pipeline
    pipe = Pipeline()
    return pipe

pipe = start_haystack()

@st.cache_data(show_spinner=True)
def query(question):
    print("Received question")
    params = {}
    # results = pipe.run(question, params=params)
    return [Answer(answer="results", context="Call  pipe.run(question, params=params) and return results in /utils/haystack.py query()")]