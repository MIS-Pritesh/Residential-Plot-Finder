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
                                  'TOTAL PLOT AREA IN SQ. FEET',
                                  rate_col,
                                  '9 % Pricing Discount Rates ( 1350 * 810 )',
                                  status_col]])
    else:
        st.warning("❌ No plots available in this budget range.")
else:
    st.info("ℹ️ Please enter a valid budget range to see available plots.")
