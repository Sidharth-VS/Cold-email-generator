import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_groq import ChatGroq
load_dotenv()
from scrape import *


class Generator:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant")

    def extract_job_details(self, url):
        content = get_webpage_text(url)
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data":content})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]
    
    def generate_mail(self, job_description, name, role, organisation, links):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are {name}, a {role}  at {organisation}.  
            Your job is to write a cold email to the client regarding the job mentioned above describing your capability 
            in fulfilling their needs.
            Also add the most relevant ones from the following links to showcase your portfolio: {link_list}
            Only include two
            Do not include projects.
            Remember you are {name}, {role} at {organisation}. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke(input={"job_description":job_description, "name":name, "role":role, "organisation":organisation, "link_list":links})
        return res.content


