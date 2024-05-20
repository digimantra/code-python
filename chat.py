import os

import qdrant_client
import streamlit as st
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Qdrant

from htmlTemplates import css, bot_template, user_template, image, footer

load_dotenv()

def clear_text():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""


def get_vectorstore(text_chunks = None):
    client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-large")
    if os.getenv("QDRANT_COLLECTION_NAME") == "openai_collection":
        embeddings = OpenAIEmbeddings()
    if os.getenv("QDRANT_COLLECTION_NAME") == "instructor_collection":
        embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vector_store = Qdrant(
        client=client, 
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"), 
        embeddings=embeddings,
    )
    if text_chunks is not None:
        vector_store.add_texts(text_chunks)
    return vector_store


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def main():

    load_dotenv()
    st.set_page_config(page_title="Personalized ChatBot",
                       page_icon=":books:",layout="centered")
   

    st.write(css,unsafe_allow_html=True)
    st.write(image, unsafe_allow_html=True)
    st.write(footer, unsafe_allow_html=True)
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Personalized ChatBot :books:")

    st.text_input(label="Ask questions about Digimantra:", key='widget', on_change=clear_text)
    user_question = st.session_state.get('my_text', '')

    if user_question:
        try:
            handle_userinput(user_question)
        except TypeError:
            st.write("Start the App First")
        except: 
            st.write("Try after some time")

    with st.sidebar:
        st.subheader("Start App")
        if st.button("Start"):
            with st.spinner("Starting"):
                try:
                    vectorstore = get_vectorstore()
                     # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vectorstore)
                    st.write("App started!")
                except Exception as e:
                
                    st.write("Unable to Connect to Database: ",e)
               
        

if __name__ == '__main__':
    main()
