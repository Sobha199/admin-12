
import streamlit as st
import pandas as pd
import time

st.set_page_config(page_title="S2M Admin Portal", layout="wide")

# Page navigation
page = st.sidebar.selectbox("Navigation", ["Login", "Dashboard", "Overview"])
st.image("s2m-logo.png", width=200)

if page == "Login":
    st.markdown("<h2 style='color:skyblue;'>Login Portal</h2>", unsafe_allow_html=True)
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter username", key="user", help="Your login ID")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="pass", help="Your password")
        submitted = st.form_submit_button("Sign In")
        if submitted:
            with st.spinner("Authenticating..."):
                time.sleep(2)
                st.success("Login successful!")

elif page == "Dashboard":
    st.markdown("<h2 style='color:skyblue;'>Admin Dashboard</h2>", unsafe_allow_html=True)
    df = pd.read_csv("Tracking.csv")
    st.markdown("## 📊 Summary Metrics")
    total_employees = df["Employee ID"].nunique()
    active = df[df["Status"].str.lower() == "active"]["User ID"].nunique()
    inactive = df[df["Status"].str.lower() == "inactive"]["User ID"].nunique()
    total_charts = df["Chart ID"].nunique() if "Chart ID" in df.columns else df.shape[0]
    total_pages = df["Pages"].sum() if "Pages" in df.columns else "N/A"
    total_icd = df["ICD"].sum() if "ICD" in df.columns else "N/A"

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Employees", total_employees)
    col2.metric("Active Employees", active)
    col3.metric("Inactive Employees", inactive)

    col4, col5, col6 = st.columns(3)
    col4.metric("Total Charts Processed", total_charts)
    col5.metric("Total Pages", total_pages)
    col6.metric("Total ICDs", total_icd)

elif page == "Overview":
    st.markdown("<h2 style='color:skyblue;'>Overview Report</h2>", unsafe_allow_html=True)
    df = pd.read_csv("Tracking.csv")
    df = df.rename(columns={
        "User ID": "Emp ID",
        "Name": "Emp Name",
        "ICD": "ICD",
        "Status": "Status",
        "Team Lead": "Team Lead"
    })

    summary = df.groupby(["Emp ID", "Emp Name", "Status", "Team Lead"]).agg({
        "Chart ID": "count",
        "ICD": "sum"
    }).reset_index().rename(columns={"Chart ID": "No of Charts"})

    st.dataframe(summary, use_container_width=True)

    emp_search = st.text_input("🔍 Search by Emp ID")
    if emp_search:
        result = summary[summary["Emp ID"].astype(str).str.contains(emp_search)]
        if not result.empty:
            st.success(f"Found {len(result)} result(s):")
            st.dataframe(result, use_container_width=True)
        else:
            st.warning("No results found.")

    csv = summary.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download Excel", csv, "overview.csv", "text/csv")
