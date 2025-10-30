from crewai import Task
import pandas as pd
from io import StringIO

# --- Task 1: Analyze the uploaded data ---
def analyze_data_function(inputs):
    """Analyze CSV data to extract key financial metrics."""
    file_data = inputs.get("file_data", "")
    df = pd.read_csv(StringIO(file_data))

    # --- Basic analysis ---
    total_rows = len(df)
    total_columns = len(df.columns)

    # --- Financial metrics (if columns exist) ---
    if "Revenue" in df.columns and "Expenses" in df.columns:
        df["Profit"] = df["Revenue"] - df["Expenses"]
        total_revenue = df["Revenue"].sum()
        total_expenses = df["Expenses"].sum()
        total_profit = df["Profit"].sum()
        avg_profit = df["Profit"].mean()
        profit_margin = (df["Profit"].sum() / df["Revenue"].sum()) * 100 if df["Revenue"].sum() != 0 else 0
        revenue_growth = (
            ((df["Revenue"].iloc[-1] - df["Revenue"].iloc[0]) / df["Revenue"].iloc[0]) * 100
            if len(df["Revenue"]) > 1 else 0
        )
    else:
        total_revenue = total_expenses = total_profit = avg_profit = profit_margin = revenue_growth = 0

    insights = {
        "total_rows": total_rows,
        "total_columns": total_columns,
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "total_profit": total_profit,
        "avg_profit": avg_profit,
        "profit_margin": profit_margin,
        "revenue_growth": revenue_growth,
    }

    return insights


# --- Task 2: Generate final structured report ---
def generate_report_function(inputs):
    """Generate a professionally formatted financial report."""
    metrics = inputs.get("analysis_results", {})

    total_revenue = metrics.get("total_revenue", 0)
    total_expenses = metrics.get("total_expenses", 0)
    total_profit = metrics.get("total_profit", 0)
    avg_profit = metrics.get("avg_profit", 0)
    profit_margin = metrics.get("profit_margin", 0)
    revenue_growth = metrics.get("revenue_growth", 0)

    # --- Structured Financial Report ---
    report_text = f"""
# 📊 Financial Performance Report

## 🧾 Executive Summary
• The organization demonstrated consistent operational activity across all quarters.  
• Revenue generation amounted to **₹{total_revenue:,.0f}**, with total expenses of **₹{total_expenses:,.0f}**.  
• Average profit stood at **₹{avg_profit:,.0f}**, reflecting a healthy profit margin of **{profit_margin:.2f}%**.  
• Overall revenue growth observed: **{revenue_growth:.2f}%** over the recorded period.

---

## 📈 Key Financial Highlights
| Metric | Value |
|:---------------------|----------------:|
| 💰 Total Revenue | ₹{total_revenue:,.0f} |
| 💸 Total Expenses | ₹{total_expenses:,.0f} |
| 🏦 Total Profit | ₹{total_profit:,.0f} |
| 📊 Average Profit | ₹{avg_profit:,.0f} |
| 💹 Profit Margin | {profit_margin:.2f}% |
| 📈 Revenue Growth | {revenue_growth:.2f}% |

---

## 🔍 Detailed Analysis
**Revenue Analysis:**  
• Revenue has shown steady movement across quarters, indicating stable income flow.  
• Growth of {revenue_growth:.2f}% from the initial to the final quarter signals positive trajectory.  

**Profitability Analysis:**  
• The average profit of ₹{avg_profit:,.0f} indicates effective cost control.  
• Profit margin of {profit_margin:.2f}% signifies moderate-to-strong financial health.  

**Expense Overview:**  
• Total expenditure of ₹{total_expenses:,.0f} was efficiently balanced against total revenue.  
• Expense-to-revenue ratio: {(total_expenses/total_revenue*100 if total_revenue != 0 else 0):.2f}%  

---

## 📊 Trend Analysis
• Profit trends align with revenue, confirming operational consistency.  
• Expense pattern remains manageable, ensuring sustainability.  
• Incremental growth potential visible with optimized resource allocation.  

---

## 🧮 Calculations & Metrics
• **Revenue Growth:** {revenue_growth:.2f}%  
• **Profit Margin:** {profit_margin:.2f}%  
• **Expense Ratio:** {(total_expenses/total_revenue*100 if total_revenue != 0 else 0):.2f}%  

---

## ✅ Conclusion
• The financials reflect a balanced and controlled fiscal period.  
• Moderate profit margins with sustained revenue inflow.  
• Strong potential for scaling with refined expense management.  

---

## 💡 Suggestions
• Diversify revenue sources to improve quarterly growth rates.  
• Optimize expense allocation to target a profit margin > {profit_margin + 5:.2f}%.  
• Strengthen financial forecasting using quarterly predictive models.  
• Invest in operational automation to reduce long-term costs.  
• Monitor quarterly KPIs to ensure performance consistency.
"""

    return {"metrics": metrics, "report": report_text}


# --- Define CrewAI Tasks ---
analyze_data = Task(
    description="Analyze the uploaded CSV data to extract revenue, expense, and profit-related insights.",
    expected_output="A structured summary of total revenue, expenses, profit, and growth rates.",
    func=analyze_data_function
)

generate_report = Task(
    description="Generate a professional, bullet-wise financial report including summary, trend analysis, calculations, and recommendations.",
    expected_output="A detailed structured report with bullet points, subheadings, and a small metrics table.",
    func=generate_report_function
)
