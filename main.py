import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
# Removed BytesIO, tempfile, and reportlab imports
from crew.workflow import run_workflow

# --- Streamlit Page Configuration ---
st.set_page_config(page_title="💼 Financial Report Generator", layout="centered")

st.title("💰 Multi-Agent Financial Report Generator")
st.write("Choose how you want to input data:")

option = st.radio("Select input method:", ("📂 Upload CSV", "✍️ Enter manually"))


# ===== FUNCTION: DISPLAY RESULTS (Updated) =====
def display_results(df, result):
    if not isinstance(result, dict):
        st.error("Unexpected output format from workflow.")
        return

    # Ensure these columns exist and are numeric before calculation
    try:
        df["Revenue"] = pd.to_numeric(df["Revenue"], errors='coerce')
        df["Expenses"] = pd.to_numeric(df["Expenses"], errors='coerce')
    except KeyError:
        st.error("Data must contain 'Revenue' and 'Expenses' columns.")
        return

    total_revenue = df["Revenue"].sum()
    total_expenses = df["Expenses"].sum()
    avg_profit = (df["Revenue"] - df["Expenses"]).mean()
    
    # Avoid division by zero
    if total_revenue == 0:
         profit_margin = 0
    else:
         profit_margin = ((df["Revenue"] - df["Expenses"]) / df["Revenue"]).mean() * 100

    st.subheader("💹 Key Financial Metrics")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("💰 Total Revenue", f"₹{total_revenue:,.0f}")
    c2.metric("💸 Total Expenses", f"₹{total_expenses:,.0f}")
    c3.metric("📈 Avg Profit", f"₹{avg_profit:,.0f}")
    c4.metric("🏦 Profit Margin", f"{profit_margin:.2f}%")

    st.subheader("📊 Visual Insights")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Line Chart
    with col1:
        fig1, ax1 = plt.subplots()
        ax1.plot(df["Quarter"], df["Revenue"], marker="o", label="Revenue")
        ax1.plot(df["Quarter"], df["Expenses"], marker="o", label="Expenses")
        ax1.set_title("Quarterly Trend")
        ax1.legend()
        st.pyplot(fig1)

    # Bar Chart
    with col2:
        fig2, ax2 = plt.subplots()
        df.plot(kind="bar", x="Quarter", y=["Revenue", "Expenses"], ax=ax2)
        ax2.set_title("Revenue vs Expenses")
        st.pyplot(fig2)

    # Pie Chart
    with col3:
        fig3, ax3 = plt.subplots()
        ax3.pie(
            [total_revenue, total_expenses],
            labels=["Revenue", "Expenses"],
            autopct="%1.1f%%",
        )
        ax3.set_title("Revenue-Expense Ratio")
        st.pyplot(fig3)

    # Profit Wave
    with col4:
        fig4, ax4 = plt.subplots()
        sns.lineplot(data=df, x="Quarter", y="Revenue", label="Revenue", ax=ax4)
        sns.lineplot(data=df, x="Quarter", y="Expenses", label="Expenses", ax=ax4)
        ax4.fill_between(df["Quarter"], df["Revenue"], df["Expenses"], alpha=0.2)
        ax4.set_title("Profit Wave")
        st.pyplot(fig4)

    report_text = result.get("report", "⚠️ No structured report found in workflow output.")
    st.subheader("🧾 Detailed Financial Report")
    st.markdown(report_text)
    
    # --- PDF Download Option REMOVED ---


# ===== STREAMLIT UI =====
if option == "📂 Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        # Read the file and ensure correct numeric types for calculations
        df = pd.read_csv(uploaded_file)
        
        # Explicitly convert Revenue and Expenses columns to numeric for charts/metrics
        try:
            df["Revenue"] = pd.to_numeric(df["Revenue"], errors='coerce')
            df["Expenses"] = pd.to_numeric(df["Expenses"], errors='coerce')
        except KeyError:
            st.error("Uploaded CSV must contain 'Quarter', 'Revenue', and 'Expenses' columns.")
            df = None # Invalidates the rest of the flow

        if df is not None:
            st.subheader("📂 Uploaded Data Preview")
            st.dataframe(df)

            if st.button("Generate Financial Report"):
                with st.spinner("Agents analyzing your financial data..."):
                    # The workflow receives the uploaded file, which can be read as a CSV
                    result = run_workflow(uploaded_file) 
                st.success("✅ Report Generated!")
                display_results(df, result)

else:
    st.write("Enter your financial data for each quarter:")
    quarters, revenues, expenses = [], [], []
    n = st.number_input(
        "How many quarters do you want to enter?", min_value=1, max_value=10, value=4
    )

    for i in range(n):
        c1, c2, c3 = st.columns(3)
        with c1:
            q = st.text_input(f"Quarter {i+1}", f"Q{i+1}")
        with c2:
            r = st.number_input(f"Revenue for {q}", min_value=0, step=1000, value=10000)
        with c3:
            e = st.number_input(f"Expenses for {q}", min_value=0, step=1000, value=5000)
        quarters.append(q)
        revenues.append(r)
        expenses.append(e)

    if st.button("Generate Financial Report"):
        df = pd.DataFrame({"Quarter": quarters, "Revenue": revenues, "Expenses": expenses})
        
        # Convert to CSV format for the multi-agent workflow
        csv_buf = StringIO()
        df.to_csv(csv_buf, index=False)
        csv_buf.seek(0)

        with st.spinner("Agents analyzing your input data..."):
            result = run_workflow(csv_buf)
        st.success("✅ Report Generated!")
        display_results(df, result)