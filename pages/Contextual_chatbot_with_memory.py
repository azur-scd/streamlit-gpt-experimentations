import streamlit as st
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader, OnlinePDFLoader, Docx2txtLoader
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import os
import tempfile

# Set Streamlit page configuration
st.set_page_config(page_title="Contextual ChatBot with memory on loaded document", layout="wide")
# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "input" not in st.session_state:
    st.session_state["input"] = ""
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []

st.title("Contextual ChatBot with memory on custom document")

MODEL = "gpt-3.5-turbo"
index = None

# Define function to get user input
def get_text():
    """
    Get the user input text.
    Returns:
        (str): The text entered by the user
    """
    return st.text_input(
        "You: ",
        st.session_state["input"],
        key="input",
        placeholder="Ask anything about the context document...",
        label_visibility="hidden",
    )

# Define function to start a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    save = []
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        save.extend(
            (
                "User:" + st.session_state["past"][i],
                "Bot:" + st.session_state["generated"][i],
            )
        )
    st.session_state["stored_session"].append(save)
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["input"] = ""
    st.session_state.entity_memory.store = {}
    st.session_state.entity_memory.buffer.clear()

@st.cache_data
def embed():
    """
    Embed the doc text into a vector.
    Returns:
        (np.array): The vector of the embedded text
    """
    pages = loader.load_and_split()
    # Load the embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=API_O)
    # Indexing
    # Save in a Vector DB
    with st.spinner("It's indexing..."):
        index = FAISS.from_documents(pages, embeddings)
    st.success("Done.", icon="✅")
    return index

cola , colb = st.columns(2)
with cola:
    option = st.selectbox(
    'How would you want to do ?',
    ('Load PDF', 'Read online PDF'))
with colb:
    API_O = st.text_input(":blue[Put Your OPENAI API-KEY :]", 
                placeholder="Paste your OpenAI API key here ",
                type="password")

if option == 'Load PDF':
    # This first step is detailed to show the text splitter step before embeddings
    # # in the two others the function load_and_split() does the job
    if uploaded_file := st.file_uploader("**Upload Your PDF File**", type=["pdf"]):
        pdf_reader = PdfReader(uploaded_file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)
        text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=4000, chunk_overlap=200, length_function=len
        )
        texts = text_splitter.split_text(text)
        # select which embeddings we want to use
        embeddings = OpenAIEmbeddings(openai_api_key=API_O)
        with st.spinner("It's indexing..."):
            index = FAISS.from_texts(texts, embeddings)
        st.success("Done.", icon="✅")
elif option == "Read online PDF":
    if file_url := st.text_input("**Paste URL then press Enter**"):
        loader = OnlinePDFLoader(file_url)
        index = embed()

if index is not None:
    llm = OpenAI(
        temperature=0, openai_api_key=API_O, model_name=MODEL, verbose=False
    )
    # Create a ConversationEntityMemory object if not already created
    st.session_state.entity_memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True, output_key="answer"
    )
    Conversation = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=index.as_retriever(),
        memory=st.session_state.entity_memory,
    )

if user_input := get_text():
    output = Conversation.run(
        {"question": user_input}
    )
    print(output)
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# Display the conversation history using an expander, and allow the user to download it
with st.expander("Conversation", expanded=True):
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        st.info(st.session_state["past"][i])
        st.success(st.session_state["generated"][i])