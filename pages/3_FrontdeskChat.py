import streamlit as st
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import random
import time
from openai import OpenAI
import os
#######################################################################################################
load_dotenv()
os.environ['OPENAI_API_KEY'] = st.secrets['API_KEY']
os.environ['LLAMA_CLOUD_API_KEY'] = st.secrets['LLAMA_CLOUD_API_KEY']
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.tools import QueryEngineTool
from llama_parse import LlamaParse
Settings.llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2)
llm = OpenAI(model="gpt-3.5-turbo", temperature=0.2)
#documents = SimpleDirectoryReader("data").load_data()
#index = VectorStoreIndex.from_documents(documents)
#query_engine = index.as_query_engine()
#############################################################################################################
# define a tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b

multiply_tool = FunctionTool.from_defaults(fn=multiply)

def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b

add_tool = FunctionTool.from_defaults(fn=add)

#summary_tool = QueryEngineTool.from_defaults(
#    query_engine,
#    name="Patient Summary",
#    description="A RAG engine with medical details about the patient")
def add_appointment(name, date, time, symptoms):

    if 'appointments_list' not in st.session_state:
        st.session_state.appointments_list = []
    st.session_state.appointments_list.append({
        'Patient Name': name,
        'Date': date, #date.strftime("%Y-%m-%d"),
        'Time': time, #time.strftime("%H:%M"),
        'Symptoms': symptoms
    })
    return "Appointment Created"
appointment_tool= FunctionTool.from_defaults(fn=add_appointment)

agent = ReActAgent.from_tools([multiply_tool, add_tool,appointment_tool], llm=llm, verbose=True)

response = agent.chat("Create appointment for midnight 2024-07-16. For using appointment tool, convert Date and time to strftime format and Patient name and symtoms as string")





#############################################################################################################

st.set_page_config(page_title="Frontdesk_Chat", page_icon="💬")
st.markdown("Chat")
st.sidebar.header("Chat")

client = OpenAI(api_key=st.secrets["API_KEY"])
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

st.title("Frontdesk Chat")



# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = agent.chat(prompt+" For using appointment tool, convert Date and time to strftime format and Patient name and symtoms as string")
    with st.chat_message("user"):
        st.markdown(prompt)
    st.write(response)
    with st.chat_message("assistant"):
        stream = client.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *[
                    {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
                ]
            ],
            stream=True,
        )

        #response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

