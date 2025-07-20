import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import io

st.set_page_config(page_title="CSV to GeoJSON Converter", layout="centered")
st.title("📍 CSV to LineString GeoJSON Converter")

# --- Session State Setup ---
if "geojson_data" not in st.session_state:
    st.session_state.geojson_data = None
if "geojson_filename" not in st.session_state:
    st.session_state.geojson_filename = None

uploaded_file = st.file_uploader("Upload your flattened CSV file", type=["csv"])
file_name_input = st.text_input("📝 Enter output file name (without .geojson):")

# --- Convert Button ---
if st.button("🚀 Convert to GeoJSON"):
    # Clear old result first
    st.session_state.geojson_data = None
    st.session_state.geojson_filename = None

    if uploaded_file is None:
        st.warning("❗ Please upload a CSV file.")
    elif not file_name_input.strip():
        st.warning("❗ Please enter output filename before downloading.")
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

            st.success("✅ GeoJSON created successfully!")

        except Exception as e:
            st.error(f"❌ Error processing file: {e}")

# --- Show Download Button If Available ---
if st.session_state.geojson_data and st.session_state.geojson_filename:
    st.download_button(
        label="⬇️ Download GeoJSON",
        data=st.session_state.geojson_data,
        file_name=st.session_state.geojson_filename,
        mime="application/geo+json"
    )
