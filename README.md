# **CAPSTONE-931: Sales Assistant Agent**

CAPSTONE-931 is a Sales Assistant Agent application powered by advanced AI technologies such as LangChain and Groq. It provides businesses with actionable insights by analyzing product data, market trends, and competitor information. This agent is designed to assist sales representatives in strategizing and optimizing their sales efforts through automated and data-driven analysis.

---

## **Features**
- **Product Analytics**:
  - Analyze and compare top competitors' products.
  - Scrape and summarize Amazon Best Sellers data.
- **Market Insights**:
  - Gather trends from Google Trends and predict future market disruptions.
  - Summarize the latest news from Google News for industry updates.
- **Custom Reports**:
  - Generate detailed sales insights based on company, product, and market data.
  - Business forecasting, including profit margins and revenue projections.
- **Ethical Analysis**:
  - Mitigates biases in decision-making processes.
  - Highlights assumptions based on limited data and promotes diverse perspectives.

---

## **Technologies Used**
- **Frontend**: [Streamlit](https://streamlit.io/) for creating an interactive user interface.
- **Backend**:
  - [LangChain](https://langchain.com/) for prompt management and model chaining.
  - [Groq](https://groq.com/) for LLM-powered insights.
- **Scraping Tools**:
  - [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for web scraping.
  - [Requests](https://docs.python-requests.org/en/master/) for fetching web data.
- **Data Visualization**: Matplotlib and Pandas for visualizing trends and generating reports.

---

## **Setup Instructions**

#### **Prerequisites**
1. Python 3.8 or higher installed on your system.
2. Install the required libraries:
   ```bash
   pip install streamlit langchain-groq langchain-core langchain-community-tools requests beautifulsoup4 pandas matplotlib
3.	Set up your Groq API Key in Streamlit secrets:
- Create a .streamlit/secrets.toml file and add:
    ```bash 
    GROQ_API_KEY = "your_groq_api_key"
#### **Running the Application**
1. Clone the repository:
    ```bash 
    git clone https://github.com/erosnol/CAPSTONE-931.git
2. Navigate to the project directory:
    ```bash 
    cd CAPSTONE-931
3. Run the Streamlit app:
    ```bash
    streamlit run app.py
4. Open the provided URL in your browser to interact with the Sales Assistant Agent.



## **Usage**
1.	Input Fields:
- Enter product information (name, category, value proposition).
- Provide URLs for competitors, Amazon best sellers, Google Trends, and Google News.
2. Generate Insights:
- Click “Generate Insights” to create a comprehensive report with actionable recommendations and business forecasts.
3. Adjust Model Behavior:
- Use the Sidebar to modify the AI model’s temperature for controlled creativity in outputs.

---


## **Example Outputs**

### Competitor Analysis Table
| **Competitor Name** | **Features**             | **Price** | **Durability** | **Comparison to Your Product**       |
|----------------------|--------------------------|-----------|----------------|---------------------------------------|
| Competitor A         | Basic ergonomic design  | $300      | Medium         | Lacks advanced features               |
| Competitor B         | Speakers, ergonomic     | $450      | High           | No immersive experience               |
| Competitor C         | Reclining, lumbar support | $350   | Medium         | Doesn't include 3D immersive features |

### Forecast Visualization
#### Projected Revenue and Profit Over 5 Years
A graph showing revenue and profit trends for the next 5 years, assuming a 10% annual growth in sales.

![Forecast Graph](forecast_example.png)

### Summary Insights
- **Amazon Best Sellers Analysis**: Identified top-performing products with comparable pricing and features.
- **Google Trends Insights**: Predicted steady growth

## **Contributing**

We welcome contributions to improve CAPSTONE-931. To get started, follow these steps:

### **Steps to Contribute**
1. **Fork the Repository**:
   - Click the "Fork" button at the top right of this repository to create your own copy.

2. **Clone the Repository**:
   - Clone your forked repository to your local machine:
     ```bash
     git clone https://github.com/your-username/CAPSTONE-931.git
     ```

3. **Create a Feature Branch**:
   - Create a new branch for your feature or bug fix:
     ```bash
     git checkout -b feature/your-feature-name
     ```

4. **Make Your Changes**:
   - Edit the code to add your feature or fix the issue.
   - Ensure your changes are well-documented and tested.

5. **Commit Your Changes**:
   - Commit your changes with a descriptive message:
     ```bash
     git commit -m "Add feature: your-feature-name"
     ```

6. **Push to Your Fork**:
   - Push your changes to your forked repository:
     ```bash
     git push origin feature/your-feature-name
     ```

7. **Create a Pull Request**:
   - Open a pull request from your feature branch to the `main` branch of the original repository.
   - Provide a clear description of the changes in the pull request.

---

### **Guidelines for Contributions**
- **Code Style**: Follow the existing coding conventions and structure.
- **Documentation**: Update the README or add comments where necessary.
- **Testing**: Ensure your changes are tested and do not break existing functionality.
- **Issues**: Reference any related issues in your pull request (e.g., `Fixes #issue-number`).

---

### **Need Help?**
If you encounter any issues or have questions about contributing, feel free to open an issue or contact the repository owner directly.

## **License**

This project is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute this software as long as the original license terms are followed.

For more information, see the [LICENSE](LICENSE) file included in this repository.

## **Acknowledgments**

This project was made possible by the following tools and technologies:

- **[Groq](https://groq.com/)**: For powering the language model integration.
- **[LangChain](https://langchain.com/)**: For seamless prompt chaining and AI agent functionalities.
- **[Streamlit](https://streamlit.io/)**: For creating an interactive and user-friendly frontend.
- **[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)**: For web scraping functionality.
- **[Pandas](https://pandas.pydata.org/)** and **[Matplotlib](https://matplotlib.org/)**: For data analysis and visualization.

A big thank you to everyone who contributed ideas, feedback, and support for this project.

## **Contact**

For any questions, feedback, or support, feel free to reach out:

- **Repository Owner**: [Erosnol](mailto:erosnol@example.com)
- **GitHub**: [CAPSTONE-931](https://github.com/erosnol/CAPSTONE-931)

We appreciate your interest in CAPSTONE-931 and look forward to your contributions!


