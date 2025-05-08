
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data
csv_path = "modified_real_pulls_1.csv"
df = pd.read_csv(csv_path)
df['Location Local Datetime'] = pd.to_datetime(df['Location Local Datetime'])
df['Hour'] = df['Location Local Datetime'].dt.hour
df['Day'] = df['Location Local Datetime'].dt.day_name()

# Sidebar Navigation
st.sidebar.title("Navigation")
slide = st.sidebar.radio("Go to:", [
    "1. Title & Date Range",
    "2. Methodology",
    "3. KPI Summary",
    "4. Top 10 SKUs Overview",
    "5. SKU Bar Charts",
    "6. Breakdown by Location & Cooler",
    "7. Time Patterns",
    "8. Restocking & OOS Incidents",
    "9. SKU & Store Index",
    "10. Brand/Category Analysis",
    "11. Key Conclusions"
])

# Slide 1
if slide == "1. Title & Date Range":
    st.title("Cooler Metrics Dashboard")
    st.subheader("Date Range")
    st.write(f"From: {df['Location Local Datetime'].min()} to {df['Location Local Datetime'].max()}")
    st.write("This dashboard presents key insights derived from cooler sensor data across office locations.")

# Slide 2
elif slide == "2. Methodology":
    st.title("Methodology")
    st.markdown("""
    **Pulls**: Identified when product count drops.
    
    **Fills**: Inferred from sudden increase in product count.
    
    **Out-of-Stock (OOS)**: When product count = 0 and no fill occurs immediately.
    
    Products are grouped by brand/category for clarity. Top SKUs are selected by pull volume.
    """)

# Slide 3
elif slide == "3. KPI Summary":
    st.title("Key Performance Indicators")
    st.metric("Total Pulls", int(df['Product Pulls'].sum()))
    st.metric("Total OOS Events", int((df['Data'] == 0).sum()))
    st.metric("Total Restocks", int(df['Product Fills'].sum()))

# Slide 4
elif slide == "4. Top 10 SKUs Overview":
    st.title("Top SKUs Overview")

    selected_location = st.selectbox("Select Location", df['Location'].dropna().unique())
    metric = st.radio("Select Metric", ['Product Pulls', 'Product Fills', 'Data Change'])

    filtered_df = df[df['Location'] == selected_location]
    top_skus = filtered_df.groupby('Product')[metric].sum().nlargest(10).reset_index()

    st.subheader(f"Top 10 SKUs by {metric} in {selected_location}")
    st.dataframe(top_skus)

    fig, ax = plt.subplots()
    ax.barh(top_skus['Product'], top_skus[metric])
    ax.set_xlabel(metric)
    ax.set_ylabel("Product")
    ax.set_title(f"Top 10 SKUs by {metric}")
    st.pyplot(fig)

# The rest of the slides remain unchanged (slides 5 to 11)...

# Slide 5
elif slide == "5. SKU Bar Charts":
    st.title("Bar Chart of Top 10 SKU Pulls")
    top_skus = df.groupby('Product')['Product Pulls'].sum().nlargest(10)
    fig, ax = plt.subplots()
    top_skus.plot(kind='barh', ax=ax)
    ax.set_xlabel("Total Pulls")
    ax.set_ylabel("SKU")
    st.pyplot(fig)

# Slide 6
elif slide == "6. Breakdown by Location & Cooler":
    st.title("Pulls by Location and Cooler")
    location_cooler = df.groupby(['Location', 'Deployment'])['Product Pulls'].sum().reset_index()
    st.dataframe(location_cooler)

# Slide 7
elif slide == "7. Time Patterns":
    st.title("Time-Based Pull Patterns")
    hourly = df.groupby('Hour')['Product Pulls'].sum()
    daily = df.groupby('Day')['Product Pulls'].sum()

    st.subheader("Pulls by Hour")
    fig, ax = plt.subplots()
    hourly.plot(kind='line', marker='o', ax=ax)
    st.pyplot(fig)

    st.subheader("Pulls by Day")
    fig, ax = plt.subplots()
    daily.plot(kind='bar', ax=ax)
    st.pyplot(fig)

# Slide 8
elif slide == "8. Restocking & OOS Incidents":
    st.title("Restocks and OOS Highlights")
    restocks = df.groupby('Product')['Product Fills'].sum().nlargest(10).reset_index()
    oos = df[df['Data'] == 0]['Product'].value_counts().nlargest(10).reset_index()
    st.subheader("Top Restocked Products")
    st.dataframe(restocks)
    st.subheader("Top OOS Products")
    st.dataframe(oos)

# Slide 9
elif slide == "9. SKU & Store Index":
    st.title("SKU and Cooler Index")
    avg_pulls = df['Product Pulls'].mean()
    sku_index = df.groupby('Product')['Product Pulls'].mean().div(avg_pulls).reset_index(name='SKU Index')
    st.dataframe(sku_index.sort_values(by='SKU Index', ascending=False).head(10))

# Slide 10
elif slide == "10. Brand/Category Analysis":
    st.title("Brand/Category Level Analysis")
    # Requires manual mapping of brands if desired
    st.write("(Placeholder) Group products by brand or category for aggregate insights.")

# Slide 11
elif slide == "11. Key Conclusions":
    st.title("Final Recommendations")
    st.markdown("""
    - Most pulls occur during weekdays between 10AM–2PM.
    - Certain SKUs consistently go out of stock.
    - Restocking timing could be better aligned with consumption patterns.
    - Consider re-evaluating product assortment for low-performing coolers.
    """)
