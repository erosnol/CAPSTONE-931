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

# Set the page configuration
st.set_page_config(
    page_title="Sales Assistant Agent",  # Tab title
    page_icon="💼",  # Optional: Emoji or URL for the favicon
    layout="centered",  # Optional: Layout can be "centered" or "wide"
    initial_sidebar_state="expanded"  # Optional: Sidebar starts expanded or collapsed
)
# Page Header
st.title(" Sales Assistant Agent")
st.markdown("Assistant Agent Powered by Groq.")

# Sidebar for settings
st.sidebar.markdown(
    "<h2 style='font-size: 24px;'>Settings</h2>", 
    unsafe_allow_html=True
)

# Dropdown to select Groq AI model
selected_groq_model = st.sidebar.selectbox(
    label="Select Groq Model",
    options=["Groq-8x7B", "Groq-8x13B", "Groq-Mixtral", "Groq-LLM"],
    help="Choose a Groq model for processing tasks."
)

temperature = st.sidebar.slider(
    label="Model Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7,
    step=0.1,
    help="Adjust the temperature to control the randomness of the model's outputs. Lower values produce more deterministic results."
)

st.sidebar.markdown("---")

# Add Google Trends link with icon
# Resources Section
st.sidebar.markdown("### Resources")
st.sidebar.markdown("[Google Trends](https://trends.google.com/)")
st.sidebar.markdown("[Google News](https://news.google.com/)")
st.sidebar.markdown("[Amazon](https://www.amazon.com/)")

st.sidebar.markdown("---")

# Add GitHub link with icon in the sidebar
st.sidebar.markdown(
    """
    <div style="display: flex; align-items: center;">
        <a href="https://github.com/erosnol/CAPSTONE-931" target="_blank" style="text-decoration: none; display: flex; align-items: center;">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" alt="GitHub Logo" width="25" style="margin-right: 10px;">
            <span style="font-size: 16px; color: white;">GitHub Repository</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

# Feedback Section at the Bottom
st.sidebar.markdown("---")  # Divider for better visual separation
with st.sidebar.expander("Provide Feedback"):
    
    
    # Feedback Text Input
    feedback = st.text_area(
        label="Feedback:",
        placeholder="Please provide any additional feedback or comments to improve results."
    )
    
    # 5-Star Rating System
    star_rating = st.slider(
        label="Rate the experience:",
        min_value=1,
        max_value=5,
        value=5,
        step=1,
        format="%d stars",
        help="Rate the application from 1 (poor) to 5 (excellent)."
    )
    
    # Feedback Submit Button
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
        # Process or save the feedback and rating here
        print(f"Feedback: {feedback}")
        print(f"Rating: {star_rating} stars")

# Align the toggle to the right using HTML and CSS
st.markdown(
    """
    <style>
    .right-align {
        display: flex;
        justify-content: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Create a container for the toggle button
with st.container():
    st.markdown('<div class="right-align">', unsafe_allow_html=True)
    demo_mode = st.checkbox("Use Demo Inputs")
    st.markdown('</div>', unsafe_allow_html=True)


# Define demo inputs
demo_inputs = {
    "product_name": "gaming chair",
    "company_url": "https://store.hermanmiller.com/gaming-view-all?lang=en_US",
    "product_category": "Office supplies",
    "competitors_url": "https://www.ewinracing.com, https://xrockergaming.com, www.razer.com, https://secretlab.co, https://www.vertagear.com/, https://www.noblechairs.com, https://www.dxracer.com, https://www.mavix.com/, https://subsonic.com/, https://www.andaseat.com/",
    "value_proposition": "a high quality 3D enhanced gaming chair for gamers with speakers, surround sound, vibrations, cupholder and Siri/Alex compatibility, priced at $399.",
    "target_customer": "Gamers",
    "amazon_best_sellers": "https://www.amazon.com/s?k=gaming+chairs&i=garden&rh=n%3A1055398%2Cp_72%3A1248915011&s=exact-aware-popularity-rank&dc&ds=v1%3AHBaNLpw8vi94y9a3WBIfMjSgF2VSI48owFQHB87fFyc&crid=ZXF6209QI6R1&qid=1734017332&rnid=1248913011&sprefix=gaming+chairs%2Caps%2C229&ref=sr_nr_p_72_1",
    "google_trends_review": "https://trends.google.com/trends/explore?geo=US&q=gaming%20chairs",
    "googled_news_search": "https://www.google.com/search?q=gaming+chairs&sca_esv=fa27aa6c1a2c9000&biw=1447&bih=750&tbm=nws&sxsrf=ADLYWIJUjMkXLxpbPMvQbSzpTvG02xCp5w%3A1734025867585&ei=iyJbZ9noIpydkPIPnqz0uQ0&ved=0ahUKEwiZ2vje5aKKAxWcDkQIHR4WPdcQ4dUDCA4&uact=5&oq=gaming+chairs&gs_lp=Egxnd3Mtd2l6LW5ld3MiDWdhbWluZyBjaGFpcnMyCxAAGIAEGLEDGIMBMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAESJYRUJAGWNMPcAJ4AJABAJgBZqAB3AaqAQQxMy4xuAEDyAEA-AEBmAIQoAL_BsICEBAAGIAEGLEDGEMYgwEYigXCAggQABiABBixA8ICChAAGIAEGEMYigXCAg0QABiABBixAxhDGIoFwgIOEAAYgAQYsQMYgwEYigXCAg0QABiABBixAxiDARgKwgIKEAAYgAQYsQMYCpgDAIgGAZIHBDE1LjGgB_FQ&sclient=gws-wiz-news"
}

# Data collection/inputs
with st.form("company_info", clear_on_submit=False):

    product_name = st.text_input(
        label="**Product Name**:",
        placeholder="Enter the product name you are selling",
        value=demo_inputs["product_name"] if demo_mode else ""
    )

    company_url = st.text_input(
        label="**Company URL**:",
        placeholder="Enter the company URL (e.g., www.company.com)",
        value=demo_inputs["company_url"] if demo_mode else ""
    )

    product_category = st.text_input(
        label="**Product Category**:",
        placeholder="Enter the product category (e.g., 'Gaming Chair', 'Cloud Storage')",
        value=demo_inputs["product_category"] if demo_mode else ""
    )

    competitors_url = st.text_input(
        label="**Competitors URL**:",
        placeholder="Enter competitor URLs separated by commas (e.g., www.apple.com, www.samsung.com)",
        value=demo_inputs["competitors_url"] if demo_mode else ""
    )

    value_proposition = st.text_input(
        label="**Value Proposition**:",
        placeholder="A sentence summarizing the product’s value",
        value=demo_inputs["value_proposition"] if demo_mode else ""
    )

    target_customer = st.text_input(
        label="**Target Customer**:",
        placeholder="Enter the target customer or audience",
        value=demo_inputs["target_customer"] if demo_mode else ""
    )

    # Product Analytics title
    st.markdown("### Specific Product Analysis")
    st.markdown("<small>Provides a product business forecast.</small>", unsafe_allow_html=True)

    amazon_best_sellers = st.text_input(
        label="**Amazon Best Sellers URL**:",
        placeholder="Enter an Amazon URL to scrape best sellers",
        value=demo_inputs["amazon_best_sellers"] if demo_mode else ""
    )

    google_trends_review = st.text_input(
        label="**Google Trends URL**:",
        placeholder="Enter a Google Trends URL for trends data",
        value=demo_inputs["google_trends_review"] if demo_mode else ""
    )

    googled_news_search = st.text_input(
        label="**Google News URL**:",
        placeholder="Enter a Google News URL for the latest news",
        value=demo_inputs["googled_news_search"] if demo_mode else ""
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
# Display the insights and download button outside the form
if company_insights:
    st.markdown(company_insights)

    # Create a download button for the report
    st.download_button(
        label="Download Report",
        data=company_insights,
        file_name="report.txt",
        mime="text/plain"
    )