import streamlit as st
import pandas as pd
import io

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
df["TOTAL_SQFT"] = df["TOTAL PLOT AREA IN SQ. FEET"]
df["TOTAL_SQMT"] = df["TOTAL PLOT AREA IN SQ. MTR"]
df["TOTAL_SQYD"] = df["TOTAL PLOT AREA IN SQ. YDS"]

# ---------------------------------
# Sidebar Clear Filter Button
# ---------------------------------
if st.button("🧹 Clear All Filters"):
    st.cache_data.clear()
    st.rerun()

# ---------------------------------
# Filters Section
# ---------------------------------
st.markdown("### 🎯 Narrow Your Search by Criteria")

col_chk1, col_chk2, col_chk3, col_chk4 = st.columns(4)

with col_chk1:
    use_budget = st.checkbox("💰 **Budget (₹)**", value=True)
with col_chk2:
    use_meter = st.checkbox("📏 **Meter (㎡)**", value=False)
with col_chk3:
    use_yard = st.checkbox("📐 **Yard (yd²)**", value=False)
with col_chk4:
    use_feet = st.checkbox("📦 **Feet (ft²)**", value=False)

filters = []

if use_budget:
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        min_budget = st.number_input("Min Budget (₹)", 0, step=10_000, value=0)
    with col_b2:
        max_budget = st.number_input("Max Budget (₹)", 1, step=10_000, value=10_000_000)

    if max_budget > min_budget:
        filters.append((df["RATE (1500)*(900)"] >= min_budget) & (df["RATE (1500)*(900)"] <= max_budget))

if use_meter:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        min_meter = st.number_input("Min Area (㎡)", 0.0, step=10.0, value=0.0)
    with col_m2:
        max_meter = st.number_input("Max Area (㎡)", 1.0, step=10.0, value=5_000.0)

    if max_meter > min_meter:
        filters.append((df["TOTAL_SQMT"] >= min_meter) & (df["TOTAL_SQMT"] <= max_meter))

if use_yard:
    col_y1, col_y2 = st.columns(2)
    with col_y1:
        min_yard = st.number_input("Min Area (yd²)", 0.0, step=10.0, value=0.0)
    with col_y2:
        max_yard = st.number_input("Max Area (yd²)", 1.0, step=10.0, value=6_000.0)

    if max_yard > min_yard:
        filters.append((df["TOTAL_SQYD"] >= min_yard) & (df["TOTAL_SQYD"] <= max_yard))

if use_feet:
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        min_feet = st.number_input("Min Area (ft²)", 0.0, step=10.0, value=0.0)
    with col_f2:
        max_feet = st.number_input("Max Area (ft²)", 1.0, step=10.0, value=50_000.0)

    if max_feet > min_feet:
        filters.append((df["TOTAL_SQFT"] >= min_feet) & (df["TOTAL_SQFT"] <= max_feet))

# ---------------------------------
# Filter Unsold and Apply All Filters
# ---------------------------------
mask = df["Status"].str.lower() != "sold out"
for f in filters:
    mask &= f

filtered_df = df[mask]

# ---------------------------------
# Display Results
# ---------------------------------
st.success(f"✅ {len(filtered_df)} plot(s) match your criteria.")

if not filtered_df.empty:
    display_cols = [
        "NO", "TOTAL PLOT AREA IN SQ. FEET", "TOTAL PLOT AREA IN SQ. MTR",
        "TOTAL PLOT AREA IN SQ. YDS", "RATE (1500)*(900)",
        "9 % Pricing Discount Rates ( 1350 * 810 )"
    ]
    st.dataframe(filtered_df[display_cols])

    # ---------------------------------
    # Download Excel
    # ---------------------------------
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        filtered_df.to_excel(writer, index=False, sheet_name="Filtered_Plots")
        writer.save()
        st.download_button(
            label="📥 Download Filtered Data as Excel",
            data=output.getvalue(),
            file_name="filtered_plots.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
else:
    st.warning("❌ No plots match the selected filters.")

# ---------------------------------
# Plot Detail Viewer
# ---------------------------------
st.markdown("---")
st.markdown("### 🔍 View Detailed Info by Plot Numbers")

plot_nos = df[df["Status"].str.lower() != "sold out"]["NO"]
plot_nos = plot_nos[pd.to_numeric(plot_nos, errors="coerce").notna()]
plot_nos = sorted(plot_nos.unique())

selected_plots = st.multiselect("Select Plot NO(s) to View Details", options=plot_nos)

if selected_plots:
    result_df = df[df["NO"].isin(selected_plots)]

    for _, row in result_df.iterrows():
        st.markdown(f"### 🏷️ Plot NO: {row['NO']}")

        def convert_area(sqft):
            sqmt = sqft / 10.7639
            sqyd = sqft / 9.0
            return sqmt, sqyd, sqft

        net_sqft = row['NET PLOT AREA IN SQ.FEET']
        built_sqft = row['BUILT UP AREA IN SQ.FEET']
        total_sqft = row['TOTAL PLOT AREA IN SQ. FEET']

        net_sqmt, net_sqyd, net_sqft = convert_area(net_sqft)
        built_sqmt, built_sqyd, built_sqft = convert_area(built_sqft)
        total_sqmt, total_sqyd, total_sqft = convert_area(total_sqft)

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

        st.write(f"**RATE (1500 × 900):** ₹{row['RATE (1500)*(900)']:,.0f}")
        st.write(f"**9% Pricing Discount (1350 × 810):** ₹{row['9 % Pricing Discount Rates ( 1350 * 810 )']:,.0f}")
        st.markdown("----")
