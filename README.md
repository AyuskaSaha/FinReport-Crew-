# 💰 Financial Insight Generator
✨ Overview
This project implements a lightweight yet powerful financial analysis application using a CrewAI multi-agent system. It leverages two specialized AI agents to handle the end-to-end process of financial report generation:

1)The Data Analyzer Agent
2)The Report Generator Agent

The application is hosted via a Streamlit interface, providing a user-friendly way to input a stock ticker and instantly receive a comprehensive financial analysis report.

# 🛠️ Installation and Setup
This guide will get your multi-agent system running locally using a Python virtual environment.

Prerequisites: 
1)Python 3.9+ is required.
2)An API Key for the Large Language Model (LLM) you are using (OpenAI).

# Step-by-Step Guide
1)Clone the Repository: 
Open your terminal (PowerShell) and clone the project:
```git clone https://github.com/AyuskaSaha/FinReport-Crew-.git```

2)Create a Virtual Environment (venv): It's best practice to create an isolated environment to manage dependencies:

```python -m venv venv```

Activate the Environment.
Your terminal prompt should show (venv) once successful.

```.\venv\Scripts\activate```

3)Install Dependencies:
Install all required packages (CrewAI, Streamlit, etc.) from the requirements.txt file:

```pip install -r requirements.txt```

4)Configure Environment Variables: Create a file named .env in the root directory and add your API key. This file is ignored by Git for security:

# Example for OpenAI
OPENAI_API_KEY="YOUR_API_KEY_HERE"

# 🏃 Usage: Running the Application
1)Once the setup is complete, you are ready to launch the Streamlit interface and generate your first financial report.

2)Ensure the Virtual Environment is Active: Verify you see (venv) at the start of your terminal prompt. If not, reactivate it:

```.\venv\Scripts\activate```

3)Run the Streamlit Application: Execute the main application file:

```streamlit run app.py```


4)Access the App: The command will automatically open a tab in your web browser.

5)Generate Report:

-->Enter the desired Stock Ticker into the input field.

-->Click the "Generate Analysis" button.

-->The CrewAI agents will coordinate, fetch data, analyze it, and the final comprehensive report will be displayed on the screen.




