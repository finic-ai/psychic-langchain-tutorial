# Psychic LangChain tutorial

This is the code for the [How to use LangChain and Psychic to answer questions about your documents with AI](https://www.psychic.dev/post/langchain-psychic-q-and-a) tutorial. There are two ways to run this app.

Psychic is a data integration platform for LLM applications. Learn more by reading the [Psychic Docs](https://docs.psychic.dev/introduction).

## Python notebook
`psychic_notebook.ipynb` is a Python notebook, which makes it easy to play around with the functionality without cloning this repo. Run it with [Google Colab](https://colab.research.google.com/) or [Jupyter Notebook](https://jupyter.org/) or just copy the hosted version [here](https://colab.research.google.com/drive/1gShmRMig-nBQYn5GBAyRDNlw8dgWbbw2?usp=sharing)

## API Server
`server.py` contains the code for setting up a HTTP server that can respond to queries about content connected through the Psychic Notion connector.

### Setup
1. Follow instructions in `.env` to configure the environment variables
2. Install [Poetry](https://python-poetry.org/docs/), if you don't already have it
3. Run the following commands
    ```bash
    poetry install
    poetry shell
    uvicorn main:app --reload
    ```
4. Test out your new API endpiont by sending a `GET` request to `http://127.0.0.1:8000/get_answer` with the following body:
    ```json
    {
      "query": "YOUR QUESTION"
    }
    ```
5. Deploy with your favorite cloud hosting provider.
