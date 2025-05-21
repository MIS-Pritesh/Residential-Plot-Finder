import streamlit as st
import pandas as pd
# Inject custom CSS to increase checkbox font size
st.markdown("""
    <style>
        /* Applies to all checkbox labels */
        label[data-testid="stCheckboxLabel"] > div {
            font-size: 18px !important;
        }
    </style>
""", unsafe_allow_html=True)

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
# SECTION 0 – extra helper columns (add once, right after you load df)
# ---------------------------
# These extra columns let us filter area in the three unit systems
df["TOTAL_SQFT"] = df["TOTAL PLOT AREA IN SQ. FEET"]
df["TOTAL_SQMT"] = df["TOTAL PLOT AREA IN SQ. MTR"]          # square-metres
df["TOTAL_SQYD"] = df["TOTAL PLOT AREA IN SQ. YDS"]              # square-yards

# ---------------------------
# SECTION 1 – Flexible Filters
# ---------------------------
st.markdown("### 🔎 Filter Your Dream Plot")

col_chk1, col_chk2, col_chk3, col_chk4 = st.columns(4)
with col_chk1:
    use_budget = st.checkbox("**<span style='font-size:18px'>Budget (₹)</span>**", value=True, unsafe_allow_html=True)
with col_chk2:
    use_meter = st.checkbox("**<span style='font-size:18px'>Meter (㎡)</span>**", unsafe_allow_html=True)
with col_chk3:
    use_yard = st.checkbox("**<span style='font-size:18px'>Yard (yd²)</span>**", unsafe_allow_html=True)
with col_chk4:
    use_feet = st.checkbox("**<span style='font-size:18px'>Feet (ft²)</span>**", unsafe_allow_html=True)


# ----  collect the user limits ------------------------------------------------
filters = []        # we’ll AND these together later

if use_budget:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        min_budget = st.number_input("Min Budget (₹)", 0, step=10_000,
                                     value=0, key="min_budget")
    with col_b2:
        max_budget = st.number_input("Max Budget (₹)", 1, step=10_000,
                                     value=10_000_000, key="max_budget")

    if max_budget > min_budget:
        filters.append(
            (df["RATE (1500)*(900)"] >= min_budget) &
            (df["RATE (1500)*(900)"] <= max_budget)
        )
    else:
        st.warning("⚠️ Max budget must be larger than min budget.")

if use_meter:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        min_meter = st.number_input("Min Area (㎡)", 0.0, step=10.0,
                                    value=0.0, key="min_meter")
    with col_m2:
        max_meter = st.number_input("Max Area (㎡)", 1.0, step=10.0,
                                    value=5_000.0, key="max_meter")

    if max_meter > min_meter:
        filters.append(
            (df["TOTAL_SQMT"] >= min_meter) & (df["TOTAL_SQMT"] <= max_meter)
        )
    else:
        st.warning("⚠️ Max ㎡ must be larger than min ㎡.")

if use_yard:
    col_y1, col_y2 = st.columns(2)
    with col_y1:
        min_yard = st.number_input("Min Area (yd²)", 0.0, step=10.0,
                                   value=0.0, key="min_yard")
    with col_y2:
        max_yard = st.number_input("Max Area (yd²)", 1.0, step=10.0,
                                   value=6_000.0, key="max_yard")

    if max_yard > min_yard:
        filters.append(
            (df["TOTAL_SQYD"] >= min_yard) & (df["TOTAL_SQYD"] <= max_yard)
        )
    else:
        st.warning("⚠️ Max yd² must be larger than min yd².")

if use_feet:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        min_feet = st.number_input("Min Area (ft²)", 0.0, step=10.0,
                                   value=0.0, key="min_feet")
    with col_f2:
        max_feet = st.number_input("Max Area (ft²)", 1.0, step=10.0,
                                   value=50_000.0, key="max_feet")

    if max_feet > min_feet:
        filters.append(
            (df["TOTAL_SQFT"] >= min_feet) & (df["TOTAL_SQFT"] <= max_feet)
        )
    else:
        st.warning("⚠️ Max ft² must be larger than min ft².")

# ---- apply all chosen filters & hide “Sold Out” plots ------------------------
mask = (df["Status"].str.lower() != "sold out")
for f in filters:
    mask &= f

filtered_df = df[mask]

# ---- feedback & table --------------------------------------------------------
st.success(f"✅ {len(filtered_df)} plot(s) match your criteria.")
if not filtered_df.empty:
    st.dataframe(filtered_df[[
        "NO",
        "TOTAL PLOT AREA IN SQ. FEET",
        "TOTAL PLOT AREA IN SQ. MTR",
        "TOTAL PLOT AREA IN SQ. YDS",
        "RATE (1500)*(900)",
        "9 % Pricing Discount Rates ( 1350 * 810 )"
    ]])
else:
    st.warning("❌ No plots match the selected filters.")

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
    
        st.write(f" **RATE (1500 × 900):** ₹{rate:,.0f}")
        st.write(f" **9% Pricing Discount (1350 × 810):** ₹{discounted_rate:,.0f}")
        st.markdown("----")
