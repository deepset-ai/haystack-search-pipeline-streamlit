import streamlit as st

from utils.config import document_store_configs, model_configs
from haystack import Pipeline
from haystack.schema import Answer
from haystack.document_stores import BaseDocumentStore
from haystack.document_stores import InMemoryDocumentStore, OpenSearchDocumentStore, WeaviateDocumentStore
from haystack.nodes import EmbeddingRetriever, FARMReader, PromptNode
from milvus_haystack import MilvusDocumentStore
#Use this file to set up your Haystack pipeline and querying

@st.cache_resource(show_spinner=False)
def start_document_store(type: str):
    #This function starts the documents store of your choice based on your command line preference
    if type == 'inmemory':
        document_store = InMemoryDocumentStore(use_bm25=True)
    elif type == 'opensearch':
        document_store = OpenSearchDocumentStore(scheme = document_store_configs['OPENSEARCH_SCHEME'], 
                                                 username = document_store_configs['OPENSEARCH_USERNAME'], 
                                                 password = document_store_configs['OPENSEARCH_PASSWORD'],
                                                 host = document_store_configs['OPENSEARCH_HOST'],
                                                 port = document_store_configs['OPENSEARCH_PORT'],
                                                 index = document_store_configs['OPENSEARCH_INDEX'],
                                                 embedding_dim = document_store_configs['OPENSEARCH_EMBEDDING_DIM'])
    elif type == 'weaviate':
        document_store = WeaviateDocumentStore(host = document_store_configs['WEAVIATE_HOST'],
                                                port = document_store_configs['WEAVIATE_PORT'],
                                                index = document_store_configs['WEAVIATE_INDEX'],
                                                embedding_dim = document_store_configs['WEAVIATE_EMBEDDING_DIM'])
    elif type == 'milvus':
        document_store = MilvusDocumentStore(uri = document_store_configs['MILVUS_URI'],
                                            index = document_store_configs['MILVUS_INDEX'],
                                            embedding_dim = document_store_configs['MILVUS_EMBEDDING_DIM'],
                                            return_embedding=True)
    return document_store

# cached to make index and models load only at start
@st.cache_resource(show_spinner=False)
def start_haystack_extractive(_document_store: BaseDocumentStore):
    retriever = EmbeddingRetriever(document_store=_document_store, 
                                   embedding_model=model_configs['EMBEDDING_MODEL'], 
                                   top_k=5)
    
    reader = FARMReader(model_name_or_path=model_configs['EXTRACTIVE_MODEL'])
    
    pipe = Pipeline()
    pipe.add_node(component=retriever, name="Retriever", inputs=["Query"])
    pipe.add_node(component=reader, name="Reader", inputs=["Retriever"])

    return pipe

@st.cache_resource(show_spinner=False)
def start_haystack_rag(_document_store: BaseDocumentStore):
    retriever = EmbeddingRetriever(document_store=_document_store, 
                                   embedding_model=model_configs['EMBEDDING_MODEL'], 
                                   top_k=5)
    
    prompt_node = PromptNode(default_prompt_template="deepset/question-answering", 
                             model_name_or_path=model_configs['GENERATIVE_MODEL'],
                             api_key=model_configs['OPENAI_KEY'])
    pipe = Pipeline()

    pipe.add_node(component=retriever, name="Retriever", inputs=["Query"])
    pipe.add_node(component=prompt_node, name="PromptNode", inputs=["Retriever"])

    return pipe

@st.cache_data(show_spinner=True)
def query(_pipeline, question):
    params = {}
    results = _pipeline.run(question, params=params)
    return results