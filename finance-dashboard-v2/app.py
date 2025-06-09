import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

# --- Income Calculation (Realistic) ---
gross_income = st.slider("Annual Gross Salary (AUD, incl. super)", 60000, 200000, 105000, step=5000)
estimated_tax_rate = 0.30  # approx for Australia
net_income = gross_income * (1 - estimated_tax_rate)
monthly_income = net_income / 12

# --- User Input Sliders ---
monthly_expense = st.slider("Monthly Expenses (AUD)", 2000, 8000, 3200, step=100)
car_budget = st.slider("Car Budget (AUD)", 10000, 100000, 50000, step=5000)
car_timeline = st.slider("Car Purchase Timeline (Months)", 1, 12, 3)
house_budget = st.slider("House Downpayment Goal (AUD)", 10000, 100000, 43200, step=2000)
house_timeline = st.slider("House Purchase Timeline (Months)", 3, 24, 10)

# --- Calculations ---
monthly_surplus = monthly_income - monthly_expense
car_savings_required = car_budget / car_timeline
house_savings_required = house_budget / house_timeline
total_required_savings = car_savings_required + house_savings_required
monthly_gap = total_required_savings - monthly_surplus

# --- Forecasting ---
if monthly_surplus > 0:
    months_to_goal = (car_budget + house_budget) / monthly_surplus
else:
    months_to_goal = float("inf")

# --- Dashboard Header ---
st.title("💸 2025 Personal Finance Goal Dashboard")

# --- Top KPIs ---
st.subheader("🔍 Financial Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Net Monthly Income", f"${monthly_income:,.2f}")
col2.metric("Monthly Surplus", f"${monthly_surplus:,.2f}")
col3.metric("Time to Hit Both Goals", f"{months_to_goal:.1f} months" if months_to_goal < 100 else "∞")

# --- Goal Status Card ---
st.markdown("### 📊 Goal Snapshot")
st.markdown(f"**Total Required Monthly Savings:** ${total_required_savings:,.2f}")
if monthly_gap <= 0:
    st.success(f"✅ You're on track! Surplus of ${-monthly_gap:,.2f}")
else:
    st.error(f"❌ Shortfall of ${monthly_gap:,.2f} — increase income or reduce goals")

# --- Plotly Chart ---
fig = go.Figure()
fig.add_trace(go.Bar(name="Surplus", x=["Cash Flow"], y=[monthly_surplus], marker_color="green"))
fig.add_trace(go.Bar(name="Required Savings", x=["Cash Flow"], y=[total_required_savings], marker_color="red"))
fig.update_layout(barmode="group", title="Monthly Surplus vs. Required Savings", height=400)
st.plotly_chart(fig)

# --- Save to CSV ---
if st.button("💾 Download This Plan as CSV"):
    today = datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame([{
        "Date": today,
        "Annual Gross Income": gross_income,
        "Estimated Net Income": net_income,
        "Monthly Income": monthly_income,
        "Monthly Expenses": monthly_expense,
        "Monthly Surplus": monthly_surplus,
        "Car Budget": car_budget,
        "Car Timeline (Months)": car_timeline,
        "House Budget": house_budget,
        "House Timeline (Months)": house_timeline,
        "Monthly Gap": monthly_gap,
        "Months to Goal": months_to_goal
    }])
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Click to Download CSV", data=csv, file_name="financial_plan_v2.csv", mime="text/csv")