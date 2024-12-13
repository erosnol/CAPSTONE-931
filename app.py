import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt



# Model and Agent tools
llm = ChatGroq(api_key=st.secrets.get("GROQ_API_KEY"))

search = TavilySearchResults(max_results=2)
parser = StrOutputParser()
# tools = [search] # add tools to the list

# Page Header
st.title(" Sales Assistant Agent")
st.markdown("Assistant Agent Powered by Groq.")

# Sidebar for settings
st.sidebar.header("Settings")
temperature = st.sidebar.slider(
    label="Model Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Adjust the temperature to control the randomness of the model's outputs. Lower values produce more deterministic results."
)

# Display the selected temperature value for confirmation
st.sidebar.markdown(f"**Current Temperature:** {temperature}")

# Data collection/inputs
with st.form("company_info", clear_on_submit=False):

    product_name = st.text_input(
    label="**Product Name**:",
    placeholder="Enter the product name you are selling"
    )

    company_url = st.text_input(
        label="**Company URL**:",
        placeholder="Enter the company URL (e.g., www.company.com)"
    )

    product_category = st.text_input(
        label="**Product Category**:",
        placeholder="Enter the product category (e.g., 'Gaming Chair', 'Cloud Storage')"
    )

    competitors_url = st.text_input(
        label="**Competitors URL**:",
        placeholder="Enter competitor URLs separated by commas (e.g., www.apple.com, www.samsung.com)"
    )

    value_proposition = st.text_input(
        label="**Value Proposition**:",
        placeholder="A sentence summarizing the product’s value"
    )

    target_customer = st.text_input(
        label="**Target Customer**:",
        placeholder="Enter the target customer or audience"
    )

    # Product Analytics title
    st.markdown("### Specific Product Analysis")
    st.markdown("<small>Provides a product business forecast.</small>", unsafe_allow_html=True)

    amazon_best_sellers = st.text_input(
        label="**Amazon Best Sellers URL**:",
        placeholder="Enter an Amazon URL to scrape best sellers"
    )

    google_trends_review = st.text_input(
        label="**Google Trends URL**:",
        placeholder="Enter a Google Trends URL for trends data"
    )

    googled_news_search = st.text_input(
        label="**Google News URL**:",
        placeholder="Enter a Google News URL for the latest news"
    )

    # Optional title
    st.markdown("### Optional")

    # File upload for document parsing
    uploaded_file = st.file_uploader("Upload a PDF or Word document for additional insights.", type=["pdf", "docx"])

    # Extra data source to scrape data
    data_source_url = st.text_input(
        label="**Additional Data Source URL**",
        placeholder="Provides a summarized insight into the provided URL"
    )

    # Feedback
    feedback = st.text_area(
        label="**Feedback**",
        placeholder="Please provide any additional feedback or comments to improve results"
    )

    # For the llm insights result
    company_insights = ""

    # Data process
    if st.form_submit_button("Generate Insights"):
        if product_name and company_url:
           with st.spinner("Processing..."):

                # Use search tool to get Company Information
                company_information = search.invoke(company_url)
                print(company_information)



                # TODO: Create prompt <=================
                prompt = """
                You are a business assistant agent tasked with generating a one-page summary to assist a sales representative in gaining insights about a prospective account. 
                Based on the inputs and additional data provided, your goal is to create a detailed and actionable report. 
                Avoid assumptions or statements that are not backed by data.
                Reflect diverse perspectives and cross-verify data when possible.
                Use the following structure:

                ### Inputs:
                - **Company Information**: {company_information}
                - **Product Name**: {product_name}
                - **Competitor URL(s)**: {competitors_url}
                - **Product Category**: {product_category}
                - **Value Proposition**: {value_proposition}
                - **Target Customer**: {target_customer}
                - **Uploaded Document**: {uploaded_file} (summarize and add insight into summary, if uploaded).
                - **Scraped Data Source**: {data_source_url} (summarize and add insight into summary, if uploaded).

                ### Tasks:
                1. **Company Strategy**:
                - Summarize the company’s activities, priorities, and any recent initiatives relevant to the product category.
                - Include mentions of key public statements, press releases, or job postings that provide insight into the company’s strategy.

                2. **Competitor Mentions**:
                - Extract and analyze data about competitors from the provided URLs and scraped data.
                - Create a **detailed comparison table** with the following columns:
                    - **Competitor Name**
                    - **Features**
                    - **Price**
                    - **Durability**
                    
                - Example table format:
                    | Competitor Name | Features                        | Price | Durability | Comparison to Your Product                    |
                    |------------------|--------------------------------|-------|------------|-----------------------------------------------|
                    | Competitor A     | Basic ergonomic design         | $500  | Medium     |   Lacks 3D immersive experience and no cupholder |
                    | Competitor B     | Speakers, ergonomic design     | $450  | High       | Lacks 3D immersive experience and cupholder   |

                3. **Leadership Information**:
                - Identify key decision-makers (e.g., CEO, CTO) and summarize relevant public statements or initiatives tied to the product category.

                4. **Product/Strategy Summary**:
                - Understand the specific characteristics of the ideal customer. Create a table with findings.
                -  Give suggestions on where the company can sell the product (sales channels).

                5. **Suggestions for Positioning**:
                - Provide recommendations for how the product can align with the company’s strategy and address the target customer’s pain points.

                6. **Product Data Analytics**:
                **Amazon Best Sellers Review**
                - Summarize top 5 products. 
                - Include the brand name, price, rating and key product features. 
                - Create a table.
                - Summarize results to see where the value proposition can provide leverage.  

                **Google Trends Review**
                - Use google_trends_review to summarize scraped data. 
                - Predict future trends and potential market disruptions
                - Create a table
                - Summarize results to see where the value proposition can provide leverage. 

                **Google Search Related News**
                - Analyze sentiment in news articles, social media posts, and customer reviews to gauge market perception. 
                - Analyze the most up to date news related to the product. Give at least 3 to 5 most up to date topics. 
                - Create a table. 
                - Summarize results to see where the value proposition can provide leverage. 

                7. **Business Value / Forecast**
                - Using all gathered inputted data to provide a business forecast on the product potential.  
                - Use a table illustrating projected profit margin and revenue everytime this prompt gets generated.
                - Use persuasive language and call-to-action phrases in the closing statement

                ## Ethical Considerations
                 - Provide actionable insights while mitigating potential biases in decision-making.
                 - Highlight areas where assumptions or extrapolations are based on limited data.
                 - Use diverse data sources (Amazon Best Sellers, Google Trends, and News Search) to ensure impartial analysis.

                ## Language and Tone 
                - Use a formal professional tone
                - Use persuasive language

                ### Final Deliverable:
                - Present the report in a structured format with clear sections:
                - **Company Strategy**
                - **Competitor Mentions (including table)**
                - **Leadership Information**
                - **Product/Strategy Summary**
                - **Recommendations for Positioning**
                - Include references or links to supporting data (articles, press releases, etc.).
                - Include a summary of identified biases, if any, and measures taken to mitigate them.
                - Present the report with fair and representative data-driven insights.

                8. ### Closing Statement:
                - Conclude the report with a persuasive note highlighting the product’s competitive edge. 
                - Use persuasive language and call-to-action phrases in the closing statement

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
                        "uploaded_file": uploaded_file,
                        "data_source_url": data_source_url,
                        "amazon_best_sellers": amazon_best_sellers,
                        "google_trends_review": google_trends_review,
                        "googled_news_search": googled_news_search
                    }
                )

    st.markdown(company_insights)