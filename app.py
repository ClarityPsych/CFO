import streamlit as st
import pandas as pd
import plotly.express as px

# Load Real-Time Claim Tracking Data
def load_claim_data():
    return pd.read_csv("real_time_claim_tracking.csv")  # Placeholder for actual data integration

# Load Payer Risk Analysis Data
def load_payer_risk_data():
    return pd.read_csv("payer_risk_analysis.csv")  # Placeholder for actual data integration

# Load Cash Flow Projection Data
def load_cash_flow_data():
    return pd.read_csv("real_time_cash_flow.csv")  # Placeholder for actual data integration

# Streamlit UI
st.title("🧠 Psychological Testing Real-Time Cash Flow Dashboard")

# Section 1: Claim Tracking
st.header("📊 Real-Time Claim Tracking")
df_claims = load_claim_data()
st.dataframe(df_claims)

# Filters for Payers and Date Range
selected_payers = st.multiselect("Filter by Payer", options=df_claims["Payer"].unique())
selected_dates = st.date_input("Select Date Range", [])
if selected_payers:
    df_claims = df_claims[df_claims["Payer"].isin(selected_payers)]
if selected_dates:
    df_claims = df_claims[(df_claims["Submission Date"] >= pd.to_datetime(selected_dates[0])) & (df_claims["Submission Date"] <= pd.to_datetime(selected_dates[1]))]
st.dataframe(df_claims)

# Section 2: Payer Risk Analysis
st.header("⚠️ Payer Risk Analysis")
df_payer_risk = load_payer_risk_data()
st.dataframe(df_payer_risk)

# Risk Visualization
fig_risk = px.bar(df_payer_risk, x="Payer", y="Risk Score", color="Risk Category",
                  title="Payer Risk Scores", labels={"Risk Score": "Average Risk Level"})
st.plotly_chart(fig_risk)

# Section 3: Cash Flow Forecast
st.header("💰 Weekly Cash Flow Forecast")
df_cash_flow = load_cash_flow_data()
st.dataframe(df_cash_flow)

# Cash Flow Visualization
fig_cashflow = px.line(df_cash_flow, x="Week Start", y="Final Adjusted Net Cash Flow ($)",
                       title="Projected Cash Flow Over 12 Weeks", markers=True)
st.plotly_chart(fig_cashflow)

# Additional Data Visualizations
st.header("📈 Additional Insights")
# Claims Status Distribution
fig_status = px.pie(df_claims, names="Status", title="Claim Status Distribution")
st.plotly_chart(fig_status)

# Payment Processing Time by Payer
fig_processing = px.box(df_claims, x="Payer", y="Processing Time (Days)", title="Payment Processing Time by Payer")
st.plotly_chart(fig_processing)

# Forecasting Trends by Insurance Group
df_forecast = df_cash_flow.groupby("Week Start").sum().reset_index()
fig_forecast = px.line(df_forecast, x="Week Start", y="Adjusted Inflows ($)", title="Projected Inflows by Insurance Group")
st.plotly_chart(fig_forecast)

# Section 4: Alerts for High-Risk Payers
st.header("🚨 High-Risk Payers & Claim Delays")
alert_payers = df_payer_risk[df_payer_risk["Risk Category"] == "High"]
if not alert_payers.empty:
    st.warning("⚠️ These payers have high risk scores and may delay payments:")
    st.dataframe(alert_payers)
else:
    st.success("✅ No high-risk payers at the moment!")

st.footer("Powered by Clarity Psychological Testing | Automated by AI")
