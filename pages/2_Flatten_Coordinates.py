import streamlit as st
import pandas as pd
import csv
import ast
from io import StringIO

st.set_page_config(page_title="Flatten Coordinates", layout="centered")
st.title("Flatten Coordinates")

# --- Session State ---
if "flattened_data" not in st.session_state:
    st.session_state.flattened_data = None
if "flattened_ready" not in st.session_state:
    st.session_state.flattened_ready = False
if "flattened_filename" not in st.session_state:
    st.session_state.flattened_filename = ""

uploaded_file = st.file_uploader("📂 Upload CSV file with road_coordinates", type=["csv"])

if uploaded_file is None and st.session_state.flattened_ready:
    st.session_state.flattened_data = None
    st.session_state.flattened_ready = False
    st.session_state.flattened_filename = ""
    st.warning("❗ Please upload CSV file first.")

file_name_input = st.text_input("📝 Enter output file name (without .csv):")

# --- Flattening Function ---
def flatten_coordinates_from_file(uploaded_file):
    output_rows = []
    content = uploaded_file.getvalue().decode('utf-8')
    lines = content.splitlines()
    header = lines[0]
    data_lines = lines[1:]

    for start in range(0, len(data_lines), 1000):
        batch_lines = data_lines[start:start + 1000]
        reader = csv.DictReader(StringIO("\n".join([header] + batch_lines)))
        for row in reader:
            try:
                coords_data = ast.literal_eval(row.get("road_coordinates", "[]"))
                if coords_data and isinstance(coords_data[0], (int, float)):
                    coords_data = [coords_data]
                for segment_index, segment_coords in enumerate(coords_data, start=1):
                    for coord in segment_coords:
                        if len(coord) < 2:
                            continue
                        output_rows.append({
                            "country_id": row.get("country_id", ""),
                            "id": row.get("id", ""),
                            "grid_id": row.get("grid_id", ""),
                            "created_at": row.get("created_at", ""),
                            "report_user_id": row.get("report_user_id", ""),
                            "type": row.get("type", ""),
                            "org_code": row.get("org_code", ""),
                            "note": row.get("note", ""),
                            "segment_id": f"{row.get('id', '')}_{segment_index}",
                            "x": coord[0],
                            "y": coord[1],
                        })
            except Exception as e:
                st.error(f"❌ Error in row {row.get('id', '')}: {e}")

    return pd.DataFrame(output_rows)

# --- Convert Button ---
if st.button("🔄 Flatten Now"):
    st.session_state.flattened_data = None
    st.session_state.flattened_ready = False
    st.session_state.flattened_filename = ""

    if uploaded_file is None:
        st.warning("❗ Please upload a CSV file.")
    elif not file_name_input.strip():
        st.warning("❗ Please enter output filename before flattening.")
    else:
        with st.spinner("⏳ Flattening..."):
            df = flatten_coordinates_from_file(uploaded_file)
            st.session_state.flattened_data = df
            filename = file_name_input.strip()
            if not filename.lower().endswith(".csv"):
                filename += ".csv"
            st.session_state.flattened_filename = filename
            st.session_state.flattened_ready = True

# --- Download Button ---
if st.session_state.flattened_ready and st.session_state.flattened_data is not None:
    st.success("✅ Coordinates flattened successfully!")
    st.download_button(
        label="⬇️ Download Flattened CSV",
        data=st.session_state.flattened_data.to_csv(index=False).encode("utf-8"),
        file_name=st.session_state.flattened_filename,
        mime="text/csv"
    )

# Footer
st.markdown(
    """
    <hr style="margin-top: 2rem; margin-bottom: 1rem;">
    <div style='text-align: center; color: grey; font-size: 0.9rem;'>
        © 2025 ID Karta IoT Team
    </div>
    """,
    unsafe_allow_html=True
)
