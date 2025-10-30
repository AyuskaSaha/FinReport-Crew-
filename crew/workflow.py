# crew/workflow.py

from crewai import Crew, Process, Task # Import Task
from .agents import DataAnalyzerAgent, ReportGeneratorAgent
# Do NOT import analyze_data, generate_report anymore, or modify them if you do
# We will define the tasks dynamically inside run_workflow.
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
import pandas as pd
# Removed: from copy import deepcopy 
# Removed: from .tasks import analyze_data, generate_report # Assuming these were Task objects

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Define your LLM using OpenAI
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)


# =========================================================
# 💡 IMPORTANT: Define the Task TEMPLATES or REMOVE the global Crew definition
# We are REMOVING the global crew definition and the deepcopy steps,
# as we will create the entire crew dynamically inside run_workflow.
# =========================================================

# If you kept the global crew, remove it now.
# crew = Crew(...) # <-- REMOVE THIS LINE


def run_workflow(file_data):
    """
    Runs the workflow: takes CSV file or text as input and returns structured results.
    """
    # --- 1. Read CSV content safely and convert to string ---
    try:
        if hasattr(file_data, "read"):
            file_data.seek(0)
            df = pd.read_csv(file_data)
        else:
            df = pd.read_csv(file_data)
    except Exception as e:
        return {"error": f"Error reading CSV: {e}"}

    data_string = df.to_csv(index=False)
    
    # --- 2. CRITICAL FIX: Instantiate NEW Tasks Dynamically ---
    
    # Task 1: Data Analysis (The agent is assigned here)
    data_task_description = f"""
        Analyze the following financial CSV data. You must derive key metrics, 
        identify trends, and summarize the performance.

        The data is:
        ---
        {data_string}
        ---

        Your analysis output MUST be thorough and ready for the Report Generator to use.
    """
    data_task = Task(
        description=data_task_description,
        agent=DataAnalyzerAgent, # Assign the agent
        expected_output="A comprehensive, bulleted analysis of the data, including trends and key findings."
    )

    # Task 2: Report Generation (The agent is assigned here and context is implied by sequential process)
    report_task = Task(
        description="""
            Based on the analysis provided by the Data Analyzer, write a professional, 
            easy-to-read financial report in markdown format. 
            The report must include an executive summary and a conclusion.
        """,
        agent=ReportGeneratorAgent, # Assign the agent
        expected_output="A final financial report in Markdown format ready for display."
    )
    
    # --- 3. Run the Crew with the Dynamic Tasks ---
    # Create the crew instance right before kickoff
    dynamic_crew = Crew(
        agents=[DataAnalyzerAgent, ReportGeneratorAgent],
        tasks=[data_task, report_task], # Use the dynamically created tasks
        process=Process.sequential,
        llm=llm,
        verbose=True # Good for debugging
    )
    
    results = dynamic_crew.kickoff() 

    # --- Extract report text and compute metrics ---
    report_text = str(getattr(results, "output", None) or results)
    
    try:
        total_revenue = df["Revenue"].sum()
        total_expenses = df["Expenses"].sum()
        profit = total_revenue - total_expenses
        avg_growth = (df["Revenue"].pct_change().mean() * 100).round(2)
        metrics = {
            "Total Revenue": f"₹{total_revenue:,.2f}",
            "Total Expenses": f"₹{total_expenses:,.2f}",
            "Profit": f"₹{profit:,.2f}",
            "Average Quarterly Growth (%)": avg_growth
        }
    except Exception as e:
        metrics = {"error": f"Metrics calculation failed: {e}"}

    return {
        "metrics": metrics,
        "report": report_text
    }