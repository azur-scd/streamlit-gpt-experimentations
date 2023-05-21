import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent

# Set Streamlit page configuration
st.set_page_config(page_title="CSV data", layout="wide")

# Set up the Streamlit app layout
st.title("Working with CSV data")

# Initialize params
MODEL = "gpt-3.5-turbo"

# Set up the Streamlit app layout
col1, col2 = st.columns(2)
with col1:
    API_O = st.text_input(
        ":blue[Put Your OPENAI API-KEY :]",
        placeholder="Paste your OpenAI API key here ",
        type="password",
    )
with col2:
    SEP_OPTION = st.selectbox("Select your CSV separator ?", (",", ";", "|"))

if not(API_O):
    st.warning("You need to set your OpenAI API-KEY")

if uploaded_file := st.file_uploader("**Upload Your CSV File**", type=["csv"]):
    df = pd.read_csv(uploaded_file, sep=SEP_OPTION, encoding="utf-8")
    st.dataframe(df)
    st.help(df)
    llm = OpenAI(temperature=0, openai_api_key=API_O, model_name=MODEL, verbose=True)
    agent = create_pandas_dataframe_agent(llm, df, verbose=False)
    if query := st.text_input("Enter your query: "):
        prompt = (
            """

            If the following query is just asking a question, reply a string as follows:
            "Answer": "answer"
            Example:
            "Answer": "The highets amount of APc is 10000 euros"

            If you do not know the answer, reply as follows:
            "Answer": "I do not know."

            if the query requires to plot a chart, use the streamlit st.bar or st.line charts.

            Below is the query.
            Query: 
            """
            + query
        )
        response = agent.run(prompt)
        response
