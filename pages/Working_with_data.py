import streamlit as st
import pandas as pd
import plotly.express as px
import json
from langchain.llms import OpenAI
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
    with st.expander("See data description"):
        st.help(df)
    llm = OpenAI(temperature=0, openai_api_key=API_O, model_name=MODEL, verbose=True)
    agent = create_pandas_dataframe_agent(llm, df, verbose=False, return_direct=True)
    if query := st.text_input("Enter your query: "):
        prompt = (
            """
            You are a assistant agent for data analysis.

            Answer the best you can to the query below, 
            and if you don't know just reply that you don't know.

            If your response is a text, use the st.success() function.
            Example : st.success("your answer")

            If the query requires to plot a chart, use the plotly.express library to draw the chart 
            and reply with the st.plotly_chart() function.
            Example : st.plotly_chart(chart)

            Below is the query.
            Query: 
            """
            + query
        )
        response = agent.run(prompt)
        #st.code(response)
        response
