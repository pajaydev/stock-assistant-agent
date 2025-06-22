import boto3
import os
import streamlit as st
from strands import Agent
from strands.models import BedrockModel
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

st.set_page_config(page_title="Stock Assistant Agent", page_icon="📈", layout="wide")

st.title("📈 Stock Assistant Agent")
st.markdown("AI-powered multi-agent assistant, powered by Strands Agent, that analyzes stocks using real-time web data and internal financial insights to answer investment queries.")

# Load environment variables
load_dotenv()

required_env_vars = ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"]
missing_env_vars = [var for var in required_env_vars if var not in os.environ]
if missing_env_vars:
    st.error(f"⚠️ Missing AWS Credentials: {', '.join(missing_env_vars)}, please add credentials to .env file")
    st.stop()

# Model name
MODEL = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"

model = BedrockModel(
    model_id=MODEL,
)

# Web Agent
web_agent = Agent(
    model=model,
    tools=[DuckDuckGoTools()],
    system_prompt="""\
        You are an experienced web researcher and news analyst! 🔍

        Follow these steps when searching for information:
        1. Start with the most recent and relevant sources
        2. Cross-reference information from multiple sources
        3. Prioritize reputable news outlets and official sources
        4. Always cite your sources with links
        5. Focus on market-moving news and significant developments
    """,
)

finance_agent = Agent(
    model=model,
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    system_prompt="""\
        You are an experienced financial analyst! 📈

        Your task is to gather and return accurate, up-to-date financial metrics for a publicly listed company

        Follow these steps when analyzing financial data:
        1. Identify the stock ticker based on the query and get most recent financial statements
        2. Cross-reference information from multiple sources
        3. Return only validated, numerical, and comparable data
        4. If data is missing, say “Data not available” and skip that item.
    """,
)

MAIN_SYSTEM_PROMPT = """
You are an AI-powered multi-agent financial assistant. Your job is to help investors answer questions about publicly listed stocks by coordinating across specialized agents.

Use web_agent to find the latest stock news, analyst sentiment, earnings, regulatory updates, and strategic announcements.
Use finance_agent to fetch financial metrics like revenue, profit margin, P/E, PEG, ROE, debt, and dividend yield.

Combine insights from all agents to assess value, growth, sentiment, and risks.

🧠 Keep responses clear, concise, and actionable. Highlight a final recommendation if relevant.
⚡️ Always highlight the final recommendation clearly (e.g., Buy / Hold / Sell) if possible.
💬 If gathering data takes time, explain what you're doing.

Optional Response Template:
Summary:
Brief summary of the company and recent developments.

📊 Financial Metrics:
Revenue growth:
P/E ratio:
Profit margin:
Debt/equity ratio:
Dividend yield:

⚠️ Risks & Considerations:

[E.g., regulatory risk, market competition, overvaluation]

💡 👉 Final Recommendation:
🟢 Buy / 🟡 Hold / 🔴 Sell — followed by one-line reasoning.
"""

# Strands Agents SDK allows easy integration of agent tools
investment_reasoning_agent = Agent(
    model=model,
    system_prompt=MAIN_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[web_agent, finance_agent]
)

query = st.text_area("", placeholder="Ask anything about a stock or company. Example: What do you think about NVIDIA?", height=100)
if st.button("🔍  Analyze") and query:
    with st.spinner("Thinking..."):
        st.session_state["query"] = query
        response = investment_reasoning_agent(query)
        st.markdown(response)
        st.session_state["response"] = response
