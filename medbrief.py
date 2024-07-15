from dotenv import load_dotenv
import os
import streamlit as st
import random
import time
load_dotenv()
os.environ['OPENAI_API_KEY'] = st.secrets['API_KEY']
os.environ['LLAMA_CLOUD_API_KEY'] = st.secrets['LLAMA_CLOUD_API_KEY']
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.tools import QueryEngineTool
from llama_parse import LlamaParse
Settings.llm = OpenAI(model="gpt-4o", temperature=0.2)
llm = OpenAI(model="gpt-4o", temperature=0.2)
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()

# parser = LlamaParse(
#     api_key="llx-PZOWtLYdpJ1b7ovFkXvFYjmA9ONqmNmFj5pKrib4RrYBKGFT",  # can also be set in your env as LLAMA_CLOUD_API_KEY
#     result_type="markdown",  # "markdown" and "text" are available
#     num_workers=4,  # if multiple files passed, split in `num_workers` API calls
#     verbose=True,
#     language="en",  # Optionally you can define a language, default=en
# )

# file_extractor = {".pdf": parser}
# documents2 = SimpleDirectoryReader(
#     "data", file_extractor=file_extractor
# ).load_data()
# index2 = VectorStoreIndex.from_documents(documents2)
# query_engine2 = index2.as_query_engine()


st.set_page_config(
    page_title="MedBrief",
    page_icon="👋",
)

patient_names = ["Nancy Dew","Karlene Hizon" ,"Henry Johnson"]

st.title('👨‍⚕️🩺🔗MedBrief')
st.markdown('<h2 style="font-size: 36px;">Dr. Bruce Wayne, Cardiologist</h2>', unsafe_allow_html=True)
name = st.selectbox("Patient Name", patient_names)
reason = st.text_area('Reason for Visit')

# define a tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and returns the product"""
    return a * b

multiply_tool = FunctionTool.from_defaults(fn=multiply)

def add(a: float, b: float) -> float:
    """Add two numbers and returns the sum"""
    return a + b

#
add_tool = FunctionTool.from_defaults(fn=add)
summary_tool = QueryEngineTool.from_defaults(
    query_engine,
    name="Patient Summary",
    description="A RAG engine with medical details about the patient named {} and keeping in mind {}".format(name,
                                                                                                             reason),
)
agent = ReActAgent.from_tools([multiply_tool, add_tool, summary_tool], llm=llm, verbose=True)
if st.button("Get Medical Summary"):
    if not name:
        st.error("Please enter the patient's name.")
    else:
        # response = agent.chat(
        # "Get medical summary qbout the patient named {} and keeping in mind {}".format(prompt_name, prompt_reason)
        # )
        st.subheader("Medical History")
        answer = query_engine.query(
            "Get a short medical summary about the patient named {} and {}.Don't show allergies and medication here".format(name, reason))
        st.write(answer.response)
        st.subheader("Relevant Tests")
        tests = query_engine.query(
            "Show blood tests or scans results on patient named {} for {}.Check only reports where {} is mentioned".format(
                name, reason, name))
        st.write(tests.response)
        st.subheader("Current Medications")
        medication = query_engine.query(
            "Tell the medication the patient named {} is taking".format(name, reason))
        st.write(medication.response)
        st.subheader("Allergies")
        allergies = query_engine.query(
            "Tell if patient named {} has any allergies".format(name, reason))
        st.write(allergies.response)
        # st.subheader("Test2")
        # response2 = query_engine2.query(
        #     "Show blood tests or scans results on patient named {} for {}.Check only reports where {} is mentioned"
        # )
        # st.write(response2)
        # if "messages" not in st.session_state:
        #     st.session_state.messages = []
        #
        # # Display chat messages from history on app rerun
        # for message in st.session_state.messages:
        #     with st.chat_message(message["role"]):
        #         st.markdown(message["content"])
        #
        # # Accept user input
        # if prompt := st.chat_input("Anything else?"):
        #     # Add user message to chat history
        #     st.session_state.messages.append({"role": "user", "content": prompt})
        #     # Display user message in chat message container
        #     with st.chat_message("user"):
        #         st.markdown(prompt)
        #
        #     # Display assistant response in chat message container
        #     with st.chat_message("assistant"):
        #         response = st.write_stream(response_generator())
        #     # Add assistant response to chat history
        #     st.session_state.messages.append({"role": "assistant", "content": response})
