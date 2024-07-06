import os
from dotenv import load_dotenv
import streamlit as st
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
# Load environment variables from the .env file
load_dotenv()
os.environ['OPENAI_API_KEY'] = st.secrets['API_KEY']
import sys
print("Python version")
print(sys.version)
Settings.llm = OpenAI(temperature=0.2, model="gpt-3.5-turbo-0125")
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext

# load some documents
documents = SimpleDirectoryReader("./data").load_data()

# initialize client, setting path to save data
db = chromadb.PersistentClient(path="./chroma_db")

# create collection
chroma_collection = db.get_or_create_collection("quickstart")

# assign chroma as the vector_store to the context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# create your index
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context
)




st.title('👨‍⚕️🩺🔗MedBrief')
st.markdown('<h2 style="font-size: 36px;">Dr. Bruce Wayne, Cardiologist</h2>', unsafe_allow_html=True)

prompt_name = st.text_input('Enter Patient name')
prompt_reason = st.text_area('Reason for Visit')

if st.button("Get Medical Summary"):
    if not prompt_name:
        st.error("Please enter the patient's name.")
    else:
        # create a query engine and query
        query_engine = index.as_query_engine()
        response = query_engine.query("Tell about the ")
        st.write(response)
        st.subheader("Medical Condition")
        st.write("Sample medical condition summary")

        st.subheader("Detected Anomalies")
        #st.write(anomalies)

        st.subheader("Current Medications")
        #st.write(medications)
