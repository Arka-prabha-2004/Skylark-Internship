# Decision Log
## Project: Monday.com Business Intelligence Agent

**Author:** Arkaprabha Chakraborty  
**Date:** March 4, 2026

---

## Overview

This document outlines the key assumptions, architectural decisions, and trade-offs made during the development of the Monday.com Business Intelligence Agent.

The goal of the system is to allow founders and executives to ask natural language questions about business performance and receive insights generated from live monday.com board data.

The system integrates sales pipeline data and operational execution data, processes it through a cleaning and analytics layer, and uses a language model to generate executive-level insights.

---

## Key Assumptions

Several assumptions were made due to ambiguity in the assignment specification.

### Board Structure

I assumed that the monday.com boards would contain structured fields that enable analysis across sales pipeline and operational execution.

The **Deals board** contains information such as:

- sector / service  
- deal value  
- deal stage  
- tentative close date  

The **Work Orders board** contains:

- execution status  
- delivery dates  
- customer code  
- work order identifiers  

These fields allow the agent to answer questions about both sales pipeline performance and operational execution.

---

### Relationship Between Boards

To support cross-board analysis, I assumed that the following fields represent the same entity:

```
Deals.client_code = WorkOrders.customer_code
```

This enables analysis such as linking pipeline deals with operational work orders.

---

### Types of Founder-Level Queries

The agent was designed around the assumption that founders typically ask high-level operational and financial questions.

Examples include:

- pipeline health  
- sector performance  
- operational execution progress  
- upcoming deal closures  
- leadership summary updates  

The system therefore prioritizes metrics relevant to executive decision-making rather than detailed operational reports.

---

## Handling Messy Data

The provided datasets contained inconsistencies such as missing values, mixed data formats, and inconsistent column naming.

To ensure reliable analysis, a preprocessing layer was implemented that:

- normalizes column names
- converts date fields to consistent datetime formats
- parses numeric values stored as text
- replaces missing values with safe defaults

This cleaning step ensures that the agent can compute reliable metrics even when board data is incomplete or inconsistent.

---

## Trade-offs and Design Decisions

Several design trade-offs were made to balance implementation time, accuracy, and system simplicity.

### LLM vs Deterministic Analytics

One key design decision was how much computation should be performed by the language model.

Two approaches were considered:

**Option A:** Let the LLM perform all analysis directly from raw tables.

**Option B:** Compute key metrics programmatically and use the LLM primarily for explanation.

The second approach was chosen.

Core metrics such as:

- total pipeline value  
- deals per sector  
- completed work orders  

are computed directly in Python before being passed to the LLM.

This reduces hallucination risk and ensures numerical accuracy, since large language models are not always reliable for performing arithmetic or aggregations directly from tabular data.

---

### Data Freshness vs Performance

The assignment requires that each user query must fetch data live from monday.com.

Because of this requirement, board data is not cached between queries.  
Each user question triggers a new API request to retrieve the latest board state.

While this slightly increases response time, it ensures that the agent always reflects current data.

---

### Prompt Design Simplicity

A single prompt structure was used rather than implementing a more complex multi-agent system or tool-calling architecture.

The prompt includes:

- computed business metrics  
- a sample of the board data  
- recent conversation context  

This approach allowed the agent to remain simple while still supporting natural language queries.

---

## What I Would Do Differently With More Time

Several improvements could be implemented with more development time.

### Advanced Query Planning

The agent could dynamically generate analytical queries against the dataframe rather than relying primarily on LLM reasoning.

This would further improve accuracy for complex questions.

---

### Improved Cross-Board Analytics

Stronger relationships between deals and work orders could allow deeper insights, such as:

- operational workload per pipeline sector  
- delivery delays affecting specific deals  
- revenue realization by execution stage  

---

### Additional Business Metrics

Potential future analytics include:

- expected pipeline revenue weighted by probability  
- deal stage conversion rates  
- work order completion rates  
- sector growth trends  

---

### Performance Optimization

API requests could be optimized using batching or partial caching strategies while still ensuring that each query retrieves the latest board state.

---

## Bonus Feature: Leadership Updates

The assignment suggested a bonus feature where the agent helps prepare leadership updates.

I interpreted **leadership updates** as concise executive summaries that synthesize key business metrics into actionable insights for founders.

This feature was implemented as a quick action within the dashboard.

When triggered, the agent generates an executive-style summary that includes:

- overall pipeline health  
- sector performance  
- operational execution progress  
- potential risks or missing data  

The system uses precomputed metrics and LLM summarization to produce concise leadership reports suitable for executive briefings.

---

## Conclusion

The final system demonstrates how an AI agent can combine live business data with natural language reasoning to provide actionable insights.

By integrating:

- live monday.com data retrieval  
- structured data cleaning  
- metric computation  
- LLM reasoning  
- conversational UI  

the agent enables founders to quickly obtain insights into pipeline health and operational performance without manual data analysis.

This approach demonstrates how conversational interfaces and live business data integrations can simplify executive decision-making by reducing the need for manual reporting and dashboard analysis.