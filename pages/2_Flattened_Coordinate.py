import streamlit as st
import pandas as pd
import csv
import ast
from io import StringIO

st.set_page_config(page_title="Flatten Coordinates", layout="centered")

# --- INIT SESSION STATE ---
for key, default in {
    "processed_data": None,
    "file_name_input": "",
    "is_processing": True,
    "last_uploaded_file_name": None,
    "is_done": True,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.title("🗺️ Flatten Coordinates CSV")

uploaded_file = st.file_uploader("📂 Upload your CSV file", type=["csv"])

# --- Detect new file upload and reset state ---
uploaded_file_changed = False
if uploaded_file is not None:
    if uploaded_file.name != st.session_state.last_uploaded_file_name:
        uploaded_file_changed = True
        st.session_state.last_uploaded_file_name = uploaded_file.name
        st.session_state.processed_data = None
        st.session_state.is_processing = False
        st.session_state.is_done = False
        st.session_state.file_name_input = ""
else:
    # No file, reset all
    st.session_state.last_uploaded_file_name = None
    st.session_state.processed_data = None
    st.session_state.is_processing = False
    st.session_state.is_done = False
    st.session_state.file_name_input = ""

# --- Core Processing Function ---
def flatten_coordinates_from_file(uploaded_file, batch_size=1000):
    try:
        st.session_state.is_processing = True
        st.session_state.is_done = False
        output_rows = []

        content = uploaded_file.getvalue().decode('utf-8')
        lines = content.splitlines()
        header = lines[0]
        data_lines = lines[1:]

        with st.spinner("⏳ Processing... Please wait."):
            for start in range(0, len(data_lines), batch_size):
                batch_lines = data_lines[start:start + batch_size]
                batch_csv = "\n".join([header] + batch_lines)
                reader = csv.DictReader(StringIO(batch_csv))

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
                                    "grid_id_clean": row.get("grid_id_clean", ""),
                                    "road_coordinates": row.get("road_coordinates", ""),
                                    "first_coordinate": row.get("first_coordinate", ""),
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
                        st.error(f"Error processing row {row.get('id', 'unknown')}: {e}")

        df = pd.DataFrame(output_rows)
        st.session_state.processed_data = df
        st.session_state.is_done = True

    except Exception as e:
        st.error(f"❌ Unexpected error occurred: {e}")
    finally:
        st.session_state.is_processing = False

# --- Floating Button Style ---
st.markdown("""
<style>
.float-btn {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 1000;
}
</style>
""", unsafe_allow_html=True)

# --- UI ---
if uploaded_file:
    st.text_input("📄 Enter output file name:", key="file_name_input")

    with st.container():
        st.markdown('<div class="float-btn">', unsafe_allow_html=True)

        if st.button("🔄 Start Flattening", disabled=st.session_state.is_processing):
            if not st.session_state.file_name_input.strip():
                st.warning("❗ Please enter filename before processing.")
            else:
                st.session_state.processed_data = None  # Hapus hasil download sebelumnya
                flatten_coordinates_from_file(uploaded_file)

        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.processed_data is not None and not st.session_state.is_processing:
        file_name = st.session_state.file_name_input.strip()
        if not file_name:
            file_name = "flattened_coordinates"
        if not file_name.lower().endswith(".csv"):
            file_name += ".csv"

        st.download_button(
            label="📥 Download CSV",
            data=st.session_state.processed_data.to_csv(index=False).encode("utf-8"),
            file_name=file_name,
            mime="text/csv",
            key="download-csv"
        )
else:
    st.info("📢 Please upload CSV data first.")
