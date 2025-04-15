# streamlit is used to create quick UI

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utlis import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    st.title("📧 Cold Mail Generator")

    # Project Description
    st.markdown("""
    ### 📌 Project Description
    Welcome to the **Cold Email Generator** — an AI-powered tool designed for companies that deploy their employees to client organizations on a **contract basis**.

    🔍 **How It Works**:  
    Just paste the URL of a company's **careers page**, and the system will:
    - Automatically extract **job openings** using advanced LLMs (LLaMA 3 via Groq),
    - Identify **required skills**,
    - Match them with your company's **portfolio/projects** using a vector database (ChromaDB),
    - And generate a **personalized cold email** tailored to the client's job requirement.

    💼 Perfect for business development teams, recruitment agencies, and staffing firms looking to **streamline communication** and **maximize placement opportunities**.

    [Click here to view the Portfolio Dataset (Skills & Project Links)](https://github.com/aditya1101raj/Ai-cold-mailing-project/blob/main/app/resource/my_portfolio.csv)
    """)

    url_input = st.text_input("Enter a URL:", value="https://asus.in/careers/aug-sept-2016/Channel_Sales_Executives.html")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
