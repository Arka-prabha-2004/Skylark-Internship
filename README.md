# Monday.com Business Intelligence Agent

This project implements an AI-powered business intelligence agent that answers natural language questions using live data from monday.com boards.

The agent integrates **sales pipeline data** and **operational execution data** to provide insights into business performance for founders and executives.

The system retrieves live data from monday.com, cleans and structures it, computes key business metrics, and uses a language model to generate natural-language insights.

---

## Architecture Overview

The system follows a layered architecture:

```
User Query
     ↓
Streamlit Chat Interface
     ↓
Agent Layer
     ↓
Monday.com API (Live Query)
     ↓
Data Parsing & Cleaning
     ↓
Business Metric Computation
     ↓
Gemini LLM Reasoning
     ↓
Natural Language Insight
```

Key components:

- **Streamlit** – conversational dashboard interface
- **Agent Layer** – query orchestration and reasoning
- **Monday.com API** – live data retrieval
- **Data Cleaning Layer** – handles messy real-world data
- **Gemini LLM** – generates executive-level insights

---

## Features

- Live monday.com board integration
- Conversational business intelligence agent
- Data cleaning for messy business datasets
- Pipeline and sector performance analysis
- Operational execution insights
- Leadership update generation
- Follow-up query support
- Visible agent action trace (debug panel)

---

## Project Structure

```
app.py              → Streamlit dashboard
agent.py            → AI agent logic
monday_api.py       → monday.com API integration
data_utils.py       → data parsing and cleaning
config.py           → board configuration
requirements.txt    → project dependencies
Decision_Log.pdf    → design decisions and trade-offs
```

---

## Monday.com Setup

1. Import the provided datasets into monday.com as two boards:

- **Deals Board** (sales pipeline data)
- **Work Orders Board** (project execution data)

2. Configure appropriate column types for:

- Date columns
- Status columns
- Numeric deal values
- Sector/service fields

3. Copy the board IDs and update them in:

```
config.py
```

Example:

```python
DEALS_BOARD_ID = YOUR_DEALS_BOARD_ID
WORK_ORDERS_BOARD_ID = YOUR_WORK_ORDERS_BOARD_ID
```

---

## Environment Variables

The application requires two API keys.

```bash
MONDAY_API_KEY
GEMINI_API_KEY
```

These can be configured using:

- environment variables
- `.env` file
- Streamlit secrets (for deployment)

Example `.env` file:

```bash
MONDAY_API_KEY=your_monday_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

## Running the Application

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your browser at:

```
http://localhost:8501
```

---

## Hosted Prototype

A deployed version of the application is available at:

```
[Hosted App Link]
```

Source monday.com boards:

```
Deals Board: [Board Link]
Work Orders Board: [Board Link]
```

---

## Example Questions

The agent can answer queries such as:

- How many deals are in the pipeline?
- Which sector has the most deals?
- Which deals are closing this quarter?
- How many work orders are completed?
- Generate a leadership update.

---

## Agent Action Trace

The interface includes an **Agent Action Trace panel** which shows the actions taken during query execution.

Example trace:

```
Fetching data from monday.com boards
Retrieved 84 deals
Retrieved 42 work orders
Analyzing business metrics
```

This ensures transparency and demonstrates that the agent is querying monday.com live for each question.

---

## License

This project was developed as part of a technical assignment and is intended for evaluation purposes.