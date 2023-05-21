import streamlit as st

# Set Streamlit page configuration
st.set_page_config(page_title="About", layout="wide")

st.title("Streamlit App around GPT")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Made with LangChain")
    st.write(
        "This language model application uses LangChain framework components to interact with GPT. The Langchain documentation for Python is available at https://python.langchain.com/en/latest/index.html"
    )

with col2:
    st.header("Components")
    st.write(
        """The application consists of 3 web pages with 3 types of implementations : chatbot, text summarization and tabular data querying"""
    )

with col3:
    st.header("API Key")
    st.write(
        "You need your personal [OpenAI API key](https://platform.openai.com/account/api-keys) to use the application. There is a [charge](https://openai.com/pricing) for using the API depending on the language model used. The cost for the gpt-3.5-turbo model used here is 0,002$ per 1000 tokens (about 750 words)."
    )

st.info(
    "This is a test and not optimized application that cannot be deployed in production as is."
)

st.divider()

# Credits
st.markdown(
    """
 <p id='credits-first-para'>Made by <a href='mailto:geraldine.geoffroy@univ-cotedazur.fr'>Géraldine Geoffroy</a></p>
 <p>Source code can be found <a href="https://github.com/azur-scd/streamli-gpt-experimentations" target="_blanck">here</a></p>
""",
    unsafe_allow_html=True,
)
