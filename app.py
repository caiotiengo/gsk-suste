import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from htmlTemplates import bot_template, user_template, css
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from transformers import pipeline
import PyPDF2

def get_pdf_text(pdf_files):
    text = ""
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def get_chunk_text(text):
    
    text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 1000,
    chunk_overlap = 200,
    length_function = len
    )

    chunks = text_splitter.split_text(text)

    return chunks


def get_vector_store(text_chunks):
    
    # For OpenAI Embeddings
    
    embeddings = OpenAIEmbeddings()
    
    # For Huggingface Embeddings

    # embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")

    vectorstore = FAISS.from_texts(texts = text_chunks, embedding = embeddings)
    
    return vectorstore

def get_conversation_chain(vector_store):
    
    # OpenAI Model

    llm = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=1)

    # HuggingFace Model

    # llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)

    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm = llm,
        retriever = vector_store.as_retriever(),
        memory = memory
    )

    return conversation_chain

def handle_user_input(question):
    if st.session_state.conversation:
        response = st.session_state.conversation({'question': question})
        st.session_state.chat_history = response['chat_history']

        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                st.markdown("""<script>scrollToForm()</script>""", unsafe_allow_html=True)

    else:
        st.error("Erro ao carregar a base de dados, tente novamente mais tarde.")

def submit():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""

def read_pdfs_in_folder(folder_path):
    pdf_contents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, "rb") as file:
                pdf_files = [file]
                pdf_text = get_pdf_text(pdf_files)
                pdf_contents.append(pdf_text)
    return pdf_contents

def combine_texts(pdf_texts):
    if len(pdf_texts) == 1:
        return pdf_texts
    else:
        combined_text = "\n\n\n".join(pdf_texts)
        return combined_text

def main():
    load_dotenv()
    st.set_page_config(page_title='Relatório de sustentabilidade', page_icon='https://99prod.s3.amazonaws.com/uploads/8fc44766-d490-47b0-9792-b9aeff8848dd/598927_541420932593531_1192935286_n.png', initial_sidebar_state = 'collapsed')

    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state or not st.session_state.conversation:
        pdf_files = read_pdfs_in_folder("./pdfs")
        #text_pdf = combine_texts(pdf_files)
        if pdf_files:
            text_chunks = get_chunk_text(pdf_files[0])
            vector_store = get_vector_store(text_chunks)
            demo = True
            st.session_state.conversation = get_conversation_chain(vector_store)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.header('Relatório de sustentabilidade')
    with st.form("Question",clear_on_submit=True):
        user_question = st.text_area("Faça a sua pergunta: ", value="", help="Exemplo: Qual é a política de sustentabilidade da empresa?", key="none")
        submitted = st.form_submit_button("Enviar ✅")
        if submitted:
            handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Arquivos carregados:")
        st.write("Os Relatórios de sustentabilidade carregados foram referentes aos anos de 2019, 2020, 2021 e 2022.")

if __name__ == '__main__':
    main()
