import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Load the prompt from prompt.txt

# st.title("Industry ")
if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None
if 'company_overview' not in st.session_state:
    st.session_state.company_overview = None
if 'initial_research_completed' not in st.session_state:
    st.session_state.initial_research_completed = False
if 'analyse_transition_risk' not in st.session_state:
    st.session_state.analyse_transition_risk = False
if 'analyse_physical_risk' not in st.session_state:
    st.session_state.analyse_physical_risk = False
if 'transition_risk' not in st.session_state:
    st.session_state.transition_risk = None
if 'physical_risk' not in st.session_state:
    st.session_state.physical_risk = None
if 'last_company_name' not in st.session_state:
    st.session_state.last_company_name = ''
if 'last_primary_location' not in st.session_state:
    st.session_state.last_primary_location = ''
if 'last_industry' not in st.session_state:
    st.session_state.last_industry = ''
    
st.markdown("""
            ### 📝Welcome to TCFD Analyst!
    ##### Your TCFD reporting assistant for transition and physical risks (more to come). 
    
    Shift the focus on climate action by
    - Reducing friction to reporting.
    - Articulating strategic business impacts of climate change to drive action.
            """)

with st.expander("Readme"):
    st.markdown("""
    ##### What Can You Expect?
    - An overview and skeletal draft of transition and physical risks.
    - Aim to save 10% - 30% of your time in drafting TCFD reports.
    - Better performance observed with larger companies with an established online presence.
    - Unsure which company to pick? [Try one from here](https://en.wikipedia.org/wiki/List_of_companies_of_Singapore#Notable_firms).

    ##### Why TCFD specifically?
    - The TCFD framework aligns business incentives with climate impact 
    - It frames climate issues in terms of risks and opportunities that impact the business; a language familiar to execs and decision makers.
    - Companies act in line with their self-interests to mitigate risks, capture opportunities, and reduce their impact on the climate.
    """)

st.markdown('<hr style="border: 1px solid lightgrey;">', unsafe_allow_html=True)
# Company details inputs
company_name = st.text_input("Enter a company name", placeholder="e.g. Cold storage")
primary_location = st.text_input("Enter the primary country of operation", placeholder="e.g. Singapore")
industry = st.text_input("Enter a short description of the company's goods/services (~5 words)", placeholder="e.g. Supermarket chain selling groceries")
st.caption("Powered by GPT-4o; rely on your own capable judgment!")

if st.session_state.get('last_company_name') != company_name or \
   st.session_state.get('last_primary_location') != primary_location or \
   st.session_state.get('last_industry') != industry:
    st.session_state.initial_research_completed = False
    st.session_state.company_overview = None
    st.session_state.analyse_transition_risk = False
    st.session_state.analyse_physical_risk = False

st.session_state.last_company_name = company_name
st.session_state.last_primary_location = primary_location
st.session_state.last_industry = industry

generate_overview = st.button("Generate company overview", use_container_width=True)

client = OpenAI(api_key=OPENAI_API_KEY)

# Display company details
if company_name and primary_location and industry and generate_overview:
    st.session_state.initial_research_completed = False
    st.session_state.company_overview = None
    with st.spinner("Context matters - Conducting research to support analysis of risks..."):
        time.sleep(3)
        overview_system_message = f"""
        You are an expert sustainability consultant specializing in sustainability reporting using the task force on climate-related financial disclosures (TCFD) framework.
        The objective is to conduct a climate risk and opportunity analysis for {company_name}, a company in the {industry} industry based in {primary_location}.
        To do so successfully, you are to provide context on {company_name} based on existing knowledge. 
        Adhere strictly to the following rules:
        - Think critically like a business strategy consultant
        - Be concise, but preserve important context for a sustainability analyst to identify climate-related opportunities and risks for TCFD reporting.
        - Summarise findings before returning any output.
        - If you don't know the answer or are unable to find a suitable answer, provide a short general description. Do not generate any false answers.
        Return responses formated in markdown.
        """
        overview_user_message = f"""
        You are to assist in sustainability reporting using the TCFD framework.
        Relying upon your extensive existing data, perform research about {company_name} as a company.
        Your research should provide an overview the following key areas:
        1. company's business operations: scope of the companys operational activities, geographical locations of operations and facilities
        2. products and services: overview of the type of products and/or services offered
        3. value chain: relevant parts of their value chain
        4. key stakeholders
        Return your findings in bulleted points, consisting of only the 4 areas above.
        Begin your answer with a one sentece summary and go straight into "1. Company's business operations"
        """
            
        overview_response = client.chat.completions.create(
            # model="gpt-3.5-turbo",
            model="gpt-4o-2024-05-13",
            stream=True,
            messages=[
                {"role": "system", "content": overview_system_message},
                {"role": "user", "content": overview_user_message},
            ]
        )
        company_overview = st.write_stream(overview_response)
        st.session_state.company_overview = company_overview

if st.session_state.initial_research_completed and st.session_state.company_overview:
# if st.session_state.company_overview:
    with st.expander("Company Overview"):
        st.write(st.session_state.company_overview)

if st.session_state.company_overview:
    col1, col2 = st.columns(2)
    with col1:
            st.session_state.analyse_transition_risk = st.button("Analyse transition risks", use_container_width=True)
    with col2:
            st.session_state.analyse_physical_risk = st.button("Analyse physical risks", use_container_width=True)

if st.session_state.analyse_transition_risk:
    st.session_state.initial_research_completed = True
    st.session_state.analyse_physical_risk = False
    transition_risk_system_message = read_file('transition_risk_system_message.txt').format(industry=industry)
    transition_risk_response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4o-2024-05-13",
        stream=True,
        messages=[
            {"role": "system", "content": transition_risk_system_message},
            {"role": "user", "content": st.session_state.company_overview},
        ]
    )

    transition_risk = st.write_stream(transition_risk_response)
    st.session_state.transition_risk = transition_risk

if st.session_state.analyse_physical_risk:
    st.session_state.initial_research_completed = True
    st.session_state.analyse_transition_risk = False
    physical_risk_system_message = read_file('physical_risk_system_message.txt').format(company=company_name, industry=industry)
    physical_risk_response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4o-2024-05-13",
        stream=True,
        messages=[
            {"role": "system", "content": physical_risk_system_message},
            {"role": "user", "content": st.session_state.company_overview},
        ]
    )

    physical_risk = st.write_stream(physical_risk_response)
    st.session_state.physical_risk = physical_risk
