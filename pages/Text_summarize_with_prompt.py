# Import necessary libraries
import streamlit as st
from langchain import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain

# Set Streamlit page configuration
st.set_page_config(page_title="Summarize document", layout="wide")

# Set up the Streamlit app layout
st.title("Summarize text in multiple languages")

# Initialize params
MODEL = "gpt-3.5-turbo"
docs = None

# Set up the Streamlit app layout
col1, col2, col3 = st.columns(3)
with col1:
    LANGUAGE = st.radio(
        "Select the language of the rendered summary", ("English", "French", "Italian")
    )
with col2:
    API_O = st.text_input(
        ":blue[Put Your OPENAI API-KEY :]",
        placeholder="Paste your OpenAI API key here ",
        type="password",
    )
with col3:
    MAX_WORDS = st.slider("Maximum number of words", 50, 516, 128)


article_text = st.text_area("Paste the text to summarize")
if st.button("Summarize"):
    text_splitter = CharacterTextSplitter(
        separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    texts = text_splitter.split_text(article_text)
    docs = [Document(page_content=t) for t in texts[:3]]

# if API_O:
if (docs is not None) & (API_O != ""):
    llm = OpenAI(temperature=0, openai_api_key=API_O, model_name=MODEL, verbose=False)
    template = """
    Write a summary og the following text:
     
    {text}

    Your abstract must not exceed {max_words} words and must be written in {language}

    """

    prompt = PromptTemplate(
        input_variables=["text", "max_words", "language"],
        template=template,
    )
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
    output = chain.run(input_documents=docs, max_words=MAX_WORDS, language=LANGUAGE)
    st.success(output)
else:
    st.warning("You need to set your OpenAI API-KEY and paset a text.")
