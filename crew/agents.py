# crew/agents.py

from crewai import Agent

# Agent that focuses on analyzing raw financial data
DataAnalyzerAgent = Agent(
    name="Data Analyzer",
    role="Analyzes uploaded financial data",
    goal="Extract meaningful insights from the uploaded CSV data such as revenue trends and expense ratios",
    backstory="A skilled data analyst specialized in interpreting company financial performance and patterns."
)

# Agent that focuses on summarizing and formatting the analysis results
ReportGeneratorAgent = Agent(
    name="Report Generator",
    role="Summarizes and presents financial insights",
    goal="Generate a concise, human-readable report from the analysis results.",
    backstory="An experienced financial advisor who creates easy-to-understand executive summaries."
)
