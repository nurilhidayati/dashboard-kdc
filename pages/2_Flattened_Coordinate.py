import streamlit as st
import pandas as pd
import csv
import ast
from io import StringIO

st.set_page_config(page_title="Flatten Coordinates", layout="centered")

# Session state to persist download state
if "processed_data" not in st.session_state:
    st.session_state.processed_data = None
if "file_name_input" not in st.session_state:
    st.session_state.file_name_input = "flattened_coordinates.csv"

def flatten_coordinates_from_file(uploaded_file, batch_size=1000):
    try:
        output_rows = []

        content = uploaded_file.getvalue().decode('utf-8')
        lines = content.splitlines()
        header = lines[0]
        data_lines = lines[1:]

        with st.spinner("⏳ Processing... Please wait."):
            for start in range(0, len(data_lines), batch_size):
                batch_lines = data_lines[start : start + batch_size]
                batch_csv = "\n".join([header] + batch_lines)
                reader = csv.DictReader(StringIO(batch_csv))

                for row in reader:
                    try:
                        coords_data = ast.literal_eval(row["road_coordinates"])
                        if coords_data and isinstance(coords_data[0][0], (int, float)):
                            coords_data = [coords_data]

                        for segment_index, segment_coords in enumerate(coords_data, start=1):
                            for coord in segment_coords:
                                output_rows.append({
                                    "country_id": row.get("country_id", ""),
                                    "id": row["id"],
                                    "grid_id": row.get("grid_id", ""),
                                    "grid_id_clean": row.get("grid_id_clean", ""),
                                    "road_coordinates": row["road_coordinates"],
                                    "first_coordinate": row.get("first_coordinate", ""),
                                    "created_at": row.get("created_at", ""),
                                    "report_user_id": row.get("report_user_id", ""),
                                    "type": row.get("type", ""),
                                    "org_code": row.get("org_code", ""),
                                    "note": row.get("note", ""),
                                    "segment_id": f"{row['id']}_{segment_index}",
                                    "x": coord[0],
                                    "y": coord[1],
                                })
                    except Exception as e:
                        st.error(f"Error processing row {row.get('id', 'unknown')}: {e}")

        df = pd.DataFrame(output_rows)
        st.session_state.processed_data = df
        st.success("✅ Done! Flattened successfully.")
        st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Unexpected error occurred: {e}")


# --- Streamlit UI ---
st.title("🗺️ Flatten Coordinates CSV")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

# Reset state when a new file is uploaded
if uploaded_file:
    st.session_state.processed_data = None

if uploaded_file:
    st.text_input("📄 Enter output file name:", value=st.session_state.file_name_input, key="file_name_input")

    if st.button("🔄 Start Flattening"):
        flatten_coordinates_from_file(uploaded_file)

# Show download button if data already processed
if st.session_state.processed_data is not None:
    csv_data = st.session_state.processed_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Flattened CSV",
        data=csv_data,
        file_name=st.session_state.file_name_input if st.session_state.file_name_input else "flattened_coordinates.csv",
        mime="text/csv"
    )
