import streamlit as st
import pandas as pd
from datetime import datetime

# --- Dashboard Header ---
st.title("💸 Personal Finance Goal Tracker")
st.markdown("An interactive simulator to calculate monthly savings needed for your car and house goals.")

# --- Sliders for User Input ---
income = st.slider("Annual Income (AUD, post-tax)", 60000, 200000, 105000, step=5000)
monthly_expense = st.slider("Monthly Expenses (AUD)", 2000, 8000, 3200, step=100)
car_budget = st.slider("Car Budget (AUD)", 10000, 100000, 50000, step=5000)
car_timeline = st.slider("Car Purchase Timeline (Months)", 1, 12, 3)
house_budget = st.slider("House Downpayment Goal (AUD)", 10000, 100000, 43200, step=2000)
house_timeline = st.slider("House Purchase Timeline (Months)", 3, 24, 10)

# --- Calculations ---
monthly_income = income / 12
car_savings_required = car_budget / car_timeline
house_savings_required = house_budget / house_timeline
total_required_savings = car_savings_required + house_savings_required
monthly_surplus = monthly_income - monthly_expense
monthly_gap = total_required_savings - monthly_surplus

# --- Output Summary ---
st.subheader("📊 Summary")
st.write(f"**Monthly Income:** ${monthly_income:,.2f}")
st.write(f"**Monthly Surplus After Expenses:** ${monthly_surplus:,.2f}")
st.write(f"**Total Required Monthly Savings for Goals:** ${total_required_savings:,.2f}")
st.write(f"**Surplus/Shortfall:** {'✅ Surplus of' if monthly_gap < 0 else '❌ Shortfall of'} ${abs(monthly_gap):,.2f}")

# --- Save Progress to CSV ---
if st.button("💾 Save Current Plan to CSV"):
    today = datetime.now().strftime("%Y-%m-%d")
    df = pd.DataFrame([{
        "Date": today,
        "Annual Income": income,
        "Monthly Expenses": monthly_expense,
        "Car Budget": car_budget,
        "Car Timeline": car_timeline,
        "House Budget": house_budget,
        "House Timeline": house_timeline,
        "Monthly Income": monthly_income,
        "Surplus After Expenses": monthly_surplus,
        "Required Savings": total_required_savings,
        "Surplus/Shortfall": monthly_gap
    }])
    df.to_csv("monthly_finance_snapshot.csv", index=False)
    st.success("Snapshot saved as CSV!")