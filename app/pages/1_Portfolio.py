import streamlit as st
from portfolio import Portfolio

portfolio_db = Portfolio() 
col1, col2 = st.columns(2)

with col1:
    tech_stack = st.text_input(label="Tech Stack", placeholder="Enter Tech Stack")
with col2:
    link = st.text_input(label="Portfolio", placeholder="Portfolio Link")

if st.button("Submit"):
    portfolio_db.store(tech_stack, link)
  