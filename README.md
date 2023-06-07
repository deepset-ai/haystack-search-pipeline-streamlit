---
title: Haystack Search Pipeline with Streamlit
emoji: 👑
colorFrom: indigo
colorTo: indigo
sdk: streamlit
sdk_version: 1.23.0
app_file: app.py
pinned: false
---

# Template Streamlit App for Haystack Search Pipelines

This template [Streamlit](https://docs.streamlit.io/) app set up for simple [Haystack search applications](https://docs.haystack.deepset.ai/docs/semantic_search) which does _nothing_ in this state.

See the ['How to use this template'](#how-to-use-this-template) instructions below to create a simple UI for your own Haystack search pipelines.

Below you will also find instructions on how you could [push this to Hugging Face Spaces 🤗](#pushing-to-hugging-face-spaces-).

## Installation and Running
To run the bare application which does _nothing_:
1. Install requirements: `pip install -r requirements.txt`
2. Run the streamlit app: `streamlit run app.py`

This will start up the app on `localhost:8501` where you will find a simple search bar. Before you start editing, you'll notice that the app will only show you instructions on what to edit:

<img width="768" alt="image" src="https://github.com/deepset-ai/haystack-search-pipeline-streamlit/assets/15802862/f38bc0ef-3828-459b-9415-d7d84c6f7ce1">

## How to use this template
1. Create a new repository from this template or simply open it in a codespace to start playing around 💙
2. Make sure your `requirements.txt` file includes the Haystack and Streamlit versions you would like to use.
3. Complete the code to include your Haystack search pipeline and return the results.
4. Make any UI edits you'd like to and [share with the Haystack community](https://haystack.deepeset.ai/community) 🥳

### Repo structure
- `./utils`: This is where we have 3 files: 
    - `config.py`: This is empty in the current state. You may use this file if you'd like to make use of any secrets such as an OpenAI key, a token for an API and so on. An example of this is in [this demo project](https://github.com/TuanaCelik/should-i-follow/blob/main/utils/config.py).
    - `haystack.py`: Here you will find some functions already set up for you to start creating your Haystack search pipeline. It includes 2 main functions called `start_haystack()` which is what we use to create a pipeline and cache it, and `query()` which is the function called by `app.py` once a user query is received.
    - `ui.py`: Use this file for any UI and initial value setups.
- `app.py`: This is the main Stremalit application file that we will run. In its current state it has a simple search bar, a 'Run' button, and a response that you can highlight answers with.

### What to edit?
1. Create your Haystack search pipeline in the `start_haystack()` function. For example and Extractive QA pipeline:

```python
#choose a document store and write documents to it
document_store = InMemoryDocumentStore() 

retriever = BM25Retreiver(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

pipe = Pipeline()
pipe.add_node(component=retriever, name="Retriever", inputs=['Query'])
pipe.add_node(component=reader, name="Reader", inputs=["Reader])
```
2. Run your Haystack search pipeline in the `query()` function and return the `results`. E.g.
```python
params = {"Retriever": {top_k: 5}}
results = pipe.run(question, params=params)
return results["answers"]
```

## Pushing to Hugging Face Spaces 🤗

Below is an example GitHub action that will let you push your Streamlit app straight to the Hugging Face Hub as a Space.

A few things to pay attention to:

1. Create a New Space on Hugging Face with the Streamlit SDK.
2. Create a Hugging Face token on your HF account.
3. Create a secret on your GitHub repo called `HF_TOKEN` and put your Hugging Face token here.
4. If you're using DocumentStores or APIs that require some keys/tokens, make sure these are provided as a secret for your HF Space too!
5. This readme is set up to tell HF spaces that it's using streamlit and that the app is running on `app.py`, make any changes to the frontmatter of this readme to display the title, emoji etc you desire.
6. Create a file in `.github/workflows/hf_sync.yml`. Here's an example that you can change with your own information, and an [example workflow](https://github.com/TuanaCelik/should-i-follow/blob/main/.github/workflows/hf_sync.yml) working for the [Should I Follow demo](https://huggingface.co/spaces/deepset/should-i-follow)

```yaml
name: Sync to Hugging Face hub
on:
  push:
    branches: [main]

  # to run this workflow manually from the Actions tab
  workflow_dispatch:

jobs:
  sync-to-hub:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
        with:
          fetch-depth: 0
          lfs: true
      - name: Push to hub
        env:
          HF_TOKEN: ${{ secrets.HF_TOKEN }}
        run: git push --force https://{YOUR_HF_USERNAME}:$HF_TOKEN@{YOUR_HF_SPACE_REPO} main
```
