import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import os

# Ensure page configuration is done first
st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")

def create_streamlit_app(llm, PortfolioFAISS, clean_text):
    st.title("📧 Cold Mail Generator")
    
    # Input field for URL
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    
    # Button to submit the URL
    submit_button = st.button("Submit")

    # On button press, process the URL
    if submit_button:
        try:
            # Use the WebBaseLoader to load data from the given URL
            loader = WebBaseLoader([url_input])
            
            # Clean and extract the content
            data = clean_text(loader.load().pop().page_content)
            
            # Load portfolio data
            PortfolioFAISS.load_portfolio()
            
            # Extract job-related data using the LLM chain
            jobs = llm.extract_jobs(data)
            
            # Loop through the jobs, extract skills, and generate emails
            for job in jobs:
                skills = job.get('skills', [])
                
                # Query portfolio for links related to the skills
                links = portfolio.query_links(skills)
                
                # Generate the email using the LLM
                email = llm.write_mail(job, links)
                
                # Display the generated email as Markdown code
                st.code(email, language='markdown')
        
        # Catch any exceptions and display the error in the Streamlit app
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    # Initialize the Chain and Portfolio objects
    chain = Chain()
    portfolio = Portfolio()

    # Load the portfolio and perform a test query for "Python"
    portfolio.load_portfolio()
    results = portfolio.query_links("Python")
    print("Query Results:", results)
    
    # Run the Streamlit app
    create_streamlit_app(chain, portfolio, clean_text)
