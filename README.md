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

This template [Streamlit](https://docs.streamlit.io/) app set up for simple [Haystack search applications](https://docs.haystack.deepset.ai/docs/semantic_search). The template is ready to do QA with **Retrievel Augmented Generation**, or **Ectractive QA**

See the ['How to use this template'](#how-to-use-this-template) instructions below to create a simple UI for your own Haystack search pipelines.

Below you will also find instructions on how you could [push this to Hugging Face Spaces 🤗](#pushing-to-hugging-face-spaces-).

## Installation and Running
To run the bare application which does _nothing_:
1. Install requirements: `pip install -r requirements.txt`
2. Run the streamlit app: `streamlit run app.py`

This will start up the app on `localhost:8501` where you will find a simple search bar. Before you start editing, you'll notice that the app will only show you instructions on what to edit.

### Optional Configurations

You can set optional cofigurations to set the:
-  `--task` you want to start the app with: `rag` or `extractive` (default: rag)
-  `--store` you want to use: `inmemory`, `opensearch`, `weaviate` or `milvus` (default: inmemory)
-  `--name` you want to have for the app. (default: 'My Search App')

E.g.:

```bash
streamlit run app.py -- --store opensearch --task extractive --name 'My Opensearch Documentation Search'
```

In a `.env` file, include all the config settings that you would like to use based on:
- The DocumentStore of your choice
- The Extractive/Generative model of your choice

While the `/utils/config.py` will create default values for some configurations, others have to be set in the `.env` such as the `OPENAI_KEY`

Example `.env`

```
OPENAI_KEY=YOUR_KEY
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L12-v2
GENERATIVE_MODEL=text-davinci-003
```


## How to use this template
1. Create a new repository from this template or simply open it in a codespace to start playing around 💙
2. Make sure your `requirements.txt` file includes the Haystack and Streamlit versions you would like to use.
3. Change the code in `utils/haystack.py` if you would like a different pipeline.
4. Create a `.env`file with all of your configuration settings.
5. Make any UI edits you'd like to and [share with the Haystack community](https://haystack.deepeset.ai/community)
6. Run the app as show in [installation and running](#installation-and-running)

### Repo structure
- `./utils`: This is where we have 3 files: 
    - `config.py`: This file extracts all of the configuration settings from a `.env` file. For some config settings, it uses default values. An example of this is in [this demo project](https://github.com/TuanaCelik/should-i-follow/blob/main/utils/config.py).
    - `haystack.py`: Here you will find some functions already set up for you to start creating your Haystack search pipeline. It includes 2 main functions called `start_haystack()` which is what we use to create a pipeline and cache it, and `query()` which is the function called by `app.py` once a user query is received.
    - `ui.py`: Use this file for any UI and initial value setups.
- `app.py`: This is the main Streamlit application file that we will run. In its current state it has a simple search bar, a 'Run' button, and a response that you can highlight answers with.

### What to edit?
There are default pipelines both in `start_haystack_extractive()` and `start_haystack_rag()`

- Change the pipelines to use the embedding models, extractive or generative models as you need.
- If using the `rag` task, change the `default_prompt_template` to use one of our available ones on [PromptHub](https://prompthub.deepset.ai) or create your own `PromptTemplate`


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
