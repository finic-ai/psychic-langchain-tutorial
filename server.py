import os
from psychicapi import ConnectorId
from langchain.document_loaders import PsychicLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from fastapi import FastAPI

# Create a document loader for google drive. We can also load from other connectors by setting the connector_id to the appropriate value e.g. ConnectorId.notion.value
# This loader uses our test credentials
google_drive_loader = PsychicLoader(
    api_key="7ddb61c1-8b6a-4d31-a58e-30d1c9ea480e", # This is your secret API key. You can get this from https://dashboard.psychic.dev/api-keys
    connector_id=ConnectorId.gdrive.value,
    connection_id="google-test-connection"
)

documents = google_drive_loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=250) ## Setting an overlap for the CharacterTextSplitter helps improve results
texts = text_splitter.split_documents(documents)

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" # Substitute your OpenAI key here. This is necessary to generate embeddings and also for making calls to OpenAI's completions endpoint

embeddings = OpenAIEmbeddings()
vdb = Chroma.from_documents(texts, embeddings)

app = FastAPI()

@app.get("/get_answer")
async def get_answer():
	chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="stuff", retriever=vdb.as_retriever())
	answer = chain({"question": "what is psychic?"}, return_only_outputs=True)
	return {"answer": answer}
