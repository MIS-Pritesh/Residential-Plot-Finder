import streamlit as st
import pandas as pd

# Load data from GitHub raw CSV
csv_url = 'https://raw.githubusercontent.com/MIS-Pritesh/Residential-Plot-Finder/main/Area%20Table%20of%20the%20Royaltan.csv'
df = pd.read_csv(csv_url)

# Convert RATE column to numeric if not already
df['RATE (1500)*(900)'] = pd.to_numeric(df['RATE (1500)*(900)'], errors='coerce')

# User input
st.title("🏡 Enter Client's Budget Range (INR)")
min_budget = st.number_input("Minimum Budget", value=600000)
max_budget = st.number_input("Maximum Budget", value=700000)

# Filter plots
filtered = df[(df['RATE (1500)*(900)'] >= min_budget) & (df['RATE (1500)*(900)'] <= max_budget)]

# Display result
if not filtered.empty:
    st.success(f"{len(filtered)} Plot(s) Available in Budget ₹{min_budget:,} - ₹{max_budget:,}")
    st.dataframe(filtered)
else:
    st.warning("❌ No plots available in this budget range.")
