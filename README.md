# Stock Assistant Agent

📈 AI-powered stock assistant using [**Strands Agent**](https://strandsagents.com/latest/) that analyzes stocks using real-time web data and financial insights.

## 📦 Prerequisites

- [`uv`](https://github.com/astral-sh/uv) installed  
```bash
curl -Ls https://astral.sh/uv/install.sh | sh
```

## Quick Start

1. Clone the repository

2. Set up Python virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

4. Install dependencies:
```bash
uv pip install -r requirements.txt
```

4. Configure aws credentails
```bash
aws configure
# OR set environment variables
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

5. Run the app:
```bash
streamlit run stock_assistant_agent.py
```

6. Open http://localhost:8501

## Usage

Enter your investment query (e.g., "Should I buy AAPL stock?") and get structured analysis with:
- Financial metrics
- Risk considerations  
- Investment recommendations

## Architecture

- **Web Agent**: Searches for recent news and market sentiment
- **Finance Agent**: Fetches financial data using YFinance
- **Main Agent**: Coordinates analysis and generates recommendations

## Dependencies

- strands-agents: Framework for creating AI agents
- agno: Tools for web search and financial data
- streamlit: Web application framework
- python-dotenv: Environment variable management