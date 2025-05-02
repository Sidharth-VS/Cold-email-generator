import streamlit as st
from generator import Generator
from portfolio import Portfolio

generator = Generator()
portfolio = Portfolio()

col1, col2, col3 = st.columns(3)

url = st.text_input(label="URL", placeholder="Enter URL")
with col1:
    name = st.text_input(label="Name", placeholder="Enter Name")
with col2:    
    role = st.text_input(label="Role", placeholder="Enter Role")
with col3:
    organisation = st.text_input(label="Organisation", placeholder="Enter Organisation")

if st.button("Generate Mail"):
    jobs = generator.extract_job_details(url)
    for job in jobs:
        skills = job.get("skills", [])
        links = portfolio.query(skills)
        job_description = job.get("description", [])
        generated_mail = generator.generate_mail(job_description, name, role, organisation, links) 
        st.code(generated_mail, language="markdown", wrap_lines=True)

