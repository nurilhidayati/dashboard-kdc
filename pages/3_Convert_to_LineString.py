import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import io

st.set_page_config(page_title="Convert CSV Points to GeoJSON LineString", layout="centered")
st.title("Convert CSV Points to GeoJSON LineString")

# --- Session State Setup ---
if "geojson_data" not in st.session_state:
    st.session_state.geojson_data = None
if "geojson_filename" not in st.session_state:
    st.session_state.geojson_filename = None
if "geojson_ready" not in st.session_state:
    st.session_state.geojson_ready = False  # Tambahan: flag sukses

uploaded_file = st.file_uploader("Upload your flattened CSV file", type=["csv"])
# --- Reset output if user removes the uploaded file ---
if uploaded_file is None and st.session_state.geojson_ready:
    st.session_state.geojson_data = None
    st.session_state.geojson_filename = None
    st.session_state.geojson_ready = False
    st.warning("❗ Please upload CSV file first.")
    
    
file_name_input = st.text_input("📝 Enter output file name (without .geojson):")

# --- Convert Button ---
if st.button("Convert to GeoJSON"):
    # Clear previous result (selalu clear ketika tombol diklik)
    st.session_state.geojson_data = None
    st.session_state.geojson_filename = None
    st.session_state.geojson_ready = False

    if uploaded_file is None:
        st.warning("❗ Please upload a CSV file.")
    elif not file_name_input.strip():
        st.warning("❗ Please enter output filename before converting.")
    else:
        try:
            df = pd.read_csv(uploaded_file)

            # Build LineStrings
            lines = []
            metadata_rows = []
            for seg_id, group in df.groupby("segment_id"):
                coords = list(zip(group["x"], group["y"]))
                lines.append(LineString(coords))
                meta = group.iloc[0].copy()
                meta["coords"] = coords
                metadata_rows.append(meta)

            gdf_roads = gpd.GeoDataFrame(metadata_rows, geometry=lines, crs="EPSG:4326")
            gdf_singlepart = gdf_roads.explode(index_parts=False).reset_index(drop=True)
            gdf_singlepart["x"] = gdf_singlepart.geometry.apply(lambda geom: geom.coords[0][0])
            gdf_singlepart["y"] = gdf_singlepart.geometry.apply(lambda geom: geom.coords[0][1])

            # Save to in-memory GeoJSON
            buffer = io.BytesIO()
            gdf_singlepart.to_file(buffer, driver='GeoJSON')
            buffer.seek(0)

            # Save to session state
            st.session_state.geojson_data = buffer
            st.session_state.geojson_filename = (
                file_name_input.strip() + ".geojson"
                if not file_name_input.strip().lower().endswith(".geojson")
                else file_name_input.strip()
            )
            st.session_state.geojson_ready = True  # Tandai sukses

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

# --- Show Download Button If Available ---
if st.session_state.geojson_ready and st.session_state.geojson_data and st.session_state.geojson_filename:
    st.success("✅ GeoJSON created successfully!")
    st.download_button(
        label="⬇️ Download GeoJSON",
        data=st.session_state.geojson_data,
        file_name=st.session_state.geojson_filename,
        mime="application/geo+json"
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
