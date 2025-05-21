import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🏡 Residential Plot Finder by Budget Range")

# Load data
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/MIS-Pritesh/Residential-Plot-Finder/main/Area%20Table%20of%20the%20Royaltan.csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

# ---------------------------
# SECTION 1: Budget Filter
# ---------------------------
st.markdown("### 💸 Enter Client's Budget Range (INR)")
min_budget = st.number_input("Minimum Budget", min_value=0, value=0)
max_budget = st.number_input("Maximum Budget", min_value=1, value=10000000)

rate_col = "RATE (1500)*(900)"
status_col = "Status"

if max_budget > min_budget:
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
    st.info("ℹ️ Please enter a valid budget range.")

# ---------------------------
# SECTION 2: Manual Plot Detail Lookup (Independent)
# ---------------------------
st.markdown("---")
st.markdown("### 🔍 View Detailed Info by Plot Numbers")

all_plot_nos = df['NO'].dropna().unique().tolist()
selected_plots = st.multiselect("Select Plot NO(s) to View Details", options=all_plot_nos)

if selected_plots:
    result_df = df[df['NO'].isin(selected_plots)]

    for idx, row in result_df.iterrows():
        st.markdown(f"### 🏷️ Plot NO: {row['NO']}")
        st.markdown(f"""
        **Net Plot Area**  
        - SQ.MTR: {row['NET PLOT AREA IN SQ.FEET'] / 10.7639:.2f}  
        - SQ.YDS: {row['NET PLOT AREA IN SQ.FEET'] / 9.0:.2f}  
        - SQ.FEET: {row['NET PLOT AREA IN SQ.FEET']:.2f}

        **BUILT UP AREA**  
        - SQ.MTR: {row['BUILT UP AREA IN SQ.FEET'] / 10.7639:.2f}  
        - SQ.YDS: {row['BUILT UP AREA IN SQ.FEET'] / 9.0:.2f}  
        - SQ.FEET: {row['BUILT UP AREA IN SQ.FEET']:.2f}

        **TOTAL PLOT AREA**  
        - SQ.MTR: {row['TOTAL PLOT AREA IN SQ. FEET'] / 10.7639:.2f}  
        - SQ.YDS: {row['TOTAL PLOT AREA IN SQ. FEET'] / 9.0:.2f}  
        - SQ.FEET: {row['TOTAL PLOT AREA IN SQ. FEET']:.2f}

        **RATE (1500 * 900)**: ₹{row[rate_col]:,.0f}  
        **9% Pricing Discount (1350 * 810)**: ₹{row['9 % Pricing Discount Rates ( 1350 * 810 )']:,.0f}  
        """)
        st.markdown("---")
