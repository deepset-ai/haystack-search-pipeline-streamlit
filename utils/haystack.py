import streamlit as st

from haystack import Pipeline

#Use this file to set up your Haystack pipeline and querying


# cached to make index and models load only at start
@st.cache(
    hash_funcs={"builtins.SwigPyObject": lambda _: None}, allow_output_mutation=True
)
def start_haystack():
    #Use this function to contruct a pipeline
    pipe = Pipeline()
    return pipe

pipe = start_haystack()

@st.cache(allow_output_mutation=True)
def query(question):
    print("Received question")
    params = {}
    # results = pipe.run(question, params=params)
    return [{"answer": "results","context": "Call  pipe.run(question, params=params) amd return results in /utils/haystack.py query()"}]