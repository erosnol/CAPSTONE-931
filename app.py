import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults


# Model and Agent tools
llm = ChatGroq(api_key=st.secrets.get("GROQ_API_KEY"))
search = TavilySearchResults(max_results=2)
parser = StrOutputParser()
# tools = [search] # add tools to the list

# Page Header
st.title("Assistant Agent")
st.markdown("Assistant Agent Powered by Groq.")


# Data collection/inputs
with st.form("company_info", clear_on_submit=True):

    product_name = st.text_input("**Product Name** (What product are you selling?):")
    
    company_url = st.text_input(
        "**Company URL** (The URL of the company you are targeting):"
    )
    
    product_category = st.text_input(
        "**Product Category** (e.g., 'Data Warehousing' or 'Cloud Data Platform')"
    )
    
    competitors_url = st.text_input("**Competitors URL** (ex. www.apple.com):")
    
    value_proposition = st.text_input(
        "**Value Proposition** (A sentence summarizing the product’s value):"
    )
    
    target_customer = st.text_input(
        "**Target Customer** (Name of the person you are trying to sell to.) :"
    )

     # File upload for document parsing
    uploaded_file = st.file_uploader("Upload a PDF or Word document for additional insights:", type=["pdf", "docx"])

    data_source_url = st.text_input(
        "**Additional Data Source URL** (Provide a URL to scrape job postings, press releases, etc.):"
    )

    # For the llm insights result
    company_insights = ""

    # Data process
    if st.form_submit_button("Generate Insights"):
        if product_name and company_url:
            st.spinner("Processing...")

            # Use search tool to get Company Information
            company_information = search.invoke(company_url)
            print(company_information)

            # TODO: Create prompt <=================
            prompt = """
            You are a business assistant agent tasked with generating a detailed one-page report to help sales representatives position their product effectively. Based on the following inputs and additional context, provide a detailed analysis with actionable insights:

            ### Inputs:
            - **Company Information**: {company_information}
            - **Product Name**: {product_name}
            - **Competitor URL(s)**: {competitors_url}
            - **Product Category**: {product_category}
            - **Value Proposition**: {value_proposition}
            - **Target Customer**: {target_customer}
            - **Uploaded Document**: {document_text} (contains product specifications and unique selling points).
            - **Scraped Data Source**: {data_source_url} (includes competitor information, press releases, or job postings).

            ### Additional Requirements:
            - **Document Insights**: Extract and incorporate relevant information from the uploaded file `{document_text}` to enhance the analysis. 
            This document contains the product's specification sheet and unique selling points, including:
            - 3D immersive experience (speakers, vibration modes).
            - Built-in cupholder.
            - High durability.
            - Competitive pricing at $400.
            - **Competitor Insights**: Use data scraped from `{data_source_url}` to identify competitors, their features, pricing, and durability.
            - add these findings in the table

            ### Tasks:
            1. **Company Strategy**:
            - Summarize the company's primary activities, priorities, and any recent initiatives or strategies.
            2. **Competitor Mentions**:
            - Extract and analyze data about competitors from the provided URLs and scraped data.
            - Create a very detailed comparison table that includes:
                - **Competitor Name**
                - **Features**
                - **Price**
                - **Durability**
                - **Comparison to Your Product** (Highlight unique selling points like 3D immersive experience, durability, and pricing advantages).
            - Example table format:
                | Competitor Name | Features                        | Price | Durability | Comparison to Your Product                      |
                |------------------|--------------------------------|-------|------------|-----------------------------------------------|
                | Competitor A     | Basic ergonomic design         | $500  | Medium     | No 3D features, no cupholder, higher price     |
                | Competitor B     | Speakers, ergonomic design     | $450  | High       | Lacks 3D immersive experience and cupholder    |
                | Your Product     | 3D immersive, cupholder, etc.  | $400  | High       | Unique immersive experience; unbeatable value  |

            3. **Leadership Information**:
            - Identify key decision-makers in the company (e.g., CEO, CTO) and summarize relevant public statements or initiatives.
            4. **Product Insights**:
            - Emphasize the unique features and value propositions of your product based on the uploaded document and compare them with competitors.
            5. **Suggestions for Positioning**:
            - Provide clear recommendations for how the product can align with the company's strategy and address customer pain points.

            ### Final Output:
            - Use a professional, structured format with clear sections for company strategy, competitor mentions, leadership insights, and product value propositions.
            - Include references or links to any supporting data.

            ### Closing Statement:
            Conclude the report with a compelling statement emphasizing the product's competitive edge and alignment with the target company's goals. Example:
            "The unmatched combination of immersive experience, durability, and affordability positions this product as a market leader. We look forward to discussing how this innovative solution aligns with your company's goals."

            Close the analysis with:  
            Best Regards,  
            Sales Agent  


            """

            # Prompt Template
            prompt_template = ChatPromptTemplate([("system", prompt)])

            # Chain
            chain = prompt_template | llm | parser

            # Result/Insights
            company_insights = chain.invoke(
                {
                    "company_information": company_information,
                    "product_name": product_name,
                    "competitors_url": competitors_url,
                    "product_category": product_category,
                    "value_proposition": value_proposition,
                    "target_customer": target_customer,
                    "data_source_url": data_source_url, 
                    "document_text": uploaded_file,
                }
            )

st.markdown(company_insights)