import streamlit as st
import pandas as pd
from io import StringIO
import base64

def filter_by_city(df, city_name):
    """
    Filters DataFrame by city name from the 'grid_id' column.
    Assumes grid_id is space-separated and city is the 2nd part.
    """
    return df[df['grid_id'].str.split().str[1] == city_name]

# --- Streamlit UI ---
st.title("✅ Step 1: Split CSV by City Name")

uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])
city_name = st.text_input("🏙️ Please Enter City Name (e.g., Jakarta)")

if uploaded_file and city_name:
    if st.button("🚀 Process"):
        with st.spinner("⏳ Processing data... Please wait."):
            df = pd.read_csv(uploaded_file)

            if "grid_id" not in df.columns:
                st.error("❌ The uploaded CSV must contain a 'grid_id' column.")
            else:
                filtered_df = filter_by_city(df, city_name)

                st.success(f"✅ Found {len(filtered_df)} rows for city: {city_name}")
                st.dataframe(filtered_df)

                # Download button
                csv_data = filtered_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download filtered CSV",
                    data=csv_data,
                    file_name=f"{city_name}_data.csv",
                    mime="text/csv"
                )

