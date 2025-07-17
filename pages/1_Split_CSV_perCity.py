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

def generate_download_link(df, filename="filtered_data.csv"):
    """
    Creates a download link for the filtered DataFrame.
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">📥 Download filtered CSV</a>'
    return href

# --- Streamlit UI ---
st.title("📍 Split CSV by City Name from grid_id")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
city_name = st.text_input("Enter City Name (e.g., Jakarta)")

if uploaded_file and city_name:
    df = pd.read_csv(uploaded_file)

    if "grid_id" not in df.columns:
        st.error("The uploaded CSV must contain a 'grid_id' column.")
    else:
        filtered_df = filter_by_city(df, city_name)

        st.success(f"✅ Found {len(filtered_df)} rows for city: {city_name}")
        st.dataframe(filtered_df)

        # Show download button
        st.markdown(generate_download_link(filtered_df, filename=f"{city_name}_data.csv"), unsafe_allow_html=True)
