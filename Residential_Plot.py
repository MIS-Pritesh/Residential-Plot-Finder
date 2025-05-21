import streamlit as st
import pandas as pd

st.title("🏡 Residential Plot Finder by Budget Range")

# Load the CSV directly from GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/MIS-Pritesh/Residential-Plot-Finder/main/Area%20Table%20of%20the%20Royaltan.csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()  # Clean column names
    return df

df = load_data()

# Rename for easier reference (optional)
rate_col = "RATE (1500)*(900)"
status_col = "Status"

# User input: min and max budget
st.markdown("### 💸 Enter Client's Budget Range (INR)")
min_budget = st.number_input("Minimum Budget", min_value=0, value=0)
max_budget = st.number_input("Maximum Budget", min_value=1, value=1)

if max_budget > min_budget:
    # Filter for available plots within budget range
    filtered_df = df[
        (df[rate_col] >= min_budget) &
        (df[rate_col] <= max_budget) &
        (df[status_col].str.lower() != 'sold out')
    ]

    st.success(f"✅ {len(filtered_df)} Plot(s) Available in Budget ₹{min_budget:,} - ₹{max_budget:,}")

    if not filtered_df.empty:
        st.dataframe(filtered_df[['NO',
                                  'NET PLOT AREA IN SQ.FEET',
                                  'BUILT UP AREA IN SQ.FEET',
                                  'TOTAL PLOT AREA IN SQ. FEET',
                                  rate_col,
                                  '9 % Pricing Discount Rates ( 1350 * 810 )',
                                  status_col]])
    else:
        st.warning("❌ No plots available in this budget range.")
else:
    st.info("ℹ️ Please enter a valid budget range to see available plots.")
    # --- Input Number of Plots to Display Detailed View ---
st.markdown("---")
st.markdown("### 🔍 View Detailed Info for Multiple Plots")

num_plots = st.number_input("Enter Number of Plots to Show", min_value=1, max_value=len(filtered_df), step=1)

if num_plots:
    selected_plots = filtered_df.head(num_plots)

for idx, row in selected_plots.iterrows():
    st.markdown(f"### 🏷️ Plot NO: {row['NO']}")
    st.markdown(f"""
    **Net Plot Area**  
    - SQ.MTR: {row.get('NET PLOT AREA IN SQ.FEET', 'N/A') / 10.7639:.2f}  
    - SQ.YDS: {row.get('NET PLOT AREA IN SQ.FEET', 'N/A') / 9.0:.2f}  
    - SQ.FEET: {row.get('NET PLOT AREA IN SQ.FEET', 'N/A'):.2f}

    **BUILT UP AREA**  
    - SQ.MTR: {row.get('BUILT UP AREA IN SQ.FEET', 'N/A') / 10.7639:.2f}  
    - SQ.YDS: {row.get('BUILT UP AREA IN SQ.FEET', 'N/A') / 9.0:.2f}  
    - SQ.FEET: {row.get('BUILT UP AREA IN SQ.FEET', 'N/A'):.2f}

    **TOTAL PLOT AREA**  
    - SQ.MTR: {row.get('TOTAL PLOT AREA IN SQ. FEET', 'N/A') / 10.7639:.2f}  
    - SQ.YDS: {row.get('TOTAL PLOT AREA IN SQ. FEET', 'N/A') / 9.0:.2f}  
    - SQ.FEET: {row.get('TOTAL PLOT AREA IN SQ. FEET', 'N/A'):.2f}

    **RATE (1500 * 900)**: ₹{row.get(rate_col, 'N/A'):,.0f}  
    **9% Pricing Discount (1350 * 810)**: ₹{row.get('9 % Pricing Discount Rates ( 1350 * 810 )', 'N/A'):,.0f}  
    """)
    st.markdown("---")
