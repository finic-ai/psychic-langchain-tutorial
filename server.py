import os
import sys
import pdb
from dotenv import load_dotenv
load_dotenv()

from psychicapi import Psychic, ConnectorId
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from fastapi import FastAPI, Request

# Create a document loader for Notion. We can also load from other connectors e.g. ConnectorId.gdrive
psychic = Psychic(secret_key=os.getenv("PSYCHIC_SECRET_KEY"))
raw_docs = psychic.get_documents(ConnectorId.notion, "connection_id") #replace connection_id with the connection ID you set while creating a new connection at https://dashboard.psychic.dev/playground

documents = [
    Document(page_content=doc["content"], metadata={"title": doc["title"], "source": doc["uri"]},)
    for doc in raw_docs
]

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=250) ## Setting an overlap for the CharacterTextSplitter helps improve results
texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
vdb = Chroma.from_documents(texts, embeddings)

app = FastAPI()

@app.get("/get_answer")
async def get_answer(request: Request):
	chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="stuff", retriever=vdb.as_retriever())
	body = await request.json()
	query = body["query"]
	answer = chain({"question": query}, return_only_outputs=True)
	return {"answer": answer}
