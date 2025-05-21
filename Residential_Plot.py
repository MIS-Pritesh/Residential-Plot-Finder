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
    
        # Extract area in sq.ft.
        net_sqft = row['NET PLOT AREA IN SQ.FEET']
        built_sqft = row['BUILT UP AREA IN SQ.FEET']
        total_sqft = row['TOTAL PLOT AREA IN SQ. FEET']
    
        # Convert to SQ.MTR and SQ.YDS
        def convert_area(sqft):
            sqmt = sqft / 10.7639
            sqyd = sqft / 9.0
            return sqmt, sqyd, sqft
    
        net_sqmt, net_sqyd, net_sqft = convert_area(net_sqft)
        built_sqmt, built_sqyd, built_sqft = convert_area(built_sqft)
        total_sqmt, total_sqyd, total_sqft = convert_area(total_sqft)
    
        # Create 3 side-by-side columns
        col1, col2, col3 = st.columns(3)
    
        with col1:
            st.subheader("Net Plot Area")
            st.write(f"SQ.MTR: **{net_sqmt:.2f}**")
            st.write(f"SQ.YDS: **{net_sqyd:.2f}**")
            st.write(f"SQ.FEET: **{net_sqft:.2f}**")
    
        with col2:
            st.subheader("Built Up Area")
            st.write(f"SQ.MTR: **{built_sqmt:.2f}**")
            st.write(f"SQ.YDS: **{built_sqyd:.2f}**")
            st.write(f"SQ.FEET: **{built_sqft:.2f}**")
    
        with col3:
            st.subheader("Total Plot Area")
            st.write(f"SQ.MTR: **{total_sqmt:.2f}**")
            st.write(f"SQ.YDS: **{total_sqyd:.2f}**")
            st.write(f"SQ.FEET: **{total_sqft:.2f}**")
    
        st.markdown("---")
    
        # Pricing Section
        rate = row['RATE (1500)*(900)']
        discounted_rate = row['9 % Pricing Discount Rates ( 1350 * 810 )']
    
        st.write(f"💰 **RATE (1500 × 900):** ₹{rate:,.0f}")
        st.write(f"💸 **9% Pricing Discount (1350 × 810):** ₹{discounted_rate:,.0f}")
        st.markdown("----")
