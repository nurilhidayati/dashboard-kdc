import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import io

st.set_page_config(page_title="CSV to GeoJSON Converter", layout="centered")
st.title("📍 CSV to LineString GeoJSON Converter")

uploaded_file = st.file_uploader("Upload your flattened CSV file", type=["csv"])

# Input filename
file_name_input = st.text_input("📝 Enter output file name (without .geojson):")

if uploaded_file:
    if st.button("🚀 Convert to GeoJSON"):
        if not file_name_input.strip():
            st.warning("❗ Please enter output filename before downloading.")
        else:
            try:
                # Load CSV
                df = pd.read_csv(uploaded_file)

                # Group and convert to LineStrings
                lines = []
                metadata_rows = []
                for seg_id, group in df.groupby("segment_id"):
                    coords = list(zip(group["x"], group["y"]))
                    lines.append(LineString(coords))
                    meta = group.iloc[0].copy()
                    meta["coords"] = coords
                    metadata_rows.append(meta)

                # Convert to GeoDataFrame
                gdf_roads = gpd.GeoDataFrame(metadata_rows, geometry=lines, crs="EPSG:4326")
                gdf_singlepart = gdf_roads.explode(index_parts=False).reset_index(drop=True)

                # Add x/y for first point
                gdf_singlepart["x"] = gdf_singlepart.geometry.apply(lambda geom: geom.coords[0][0])
                gdf_singlepart["y"] = gdf_singlepart.geometry.apply(lambda geom: geom.coords[0][1])

                # Save to GeoJSON
                geojson_buffer = io.BytesIO()
                gdf_singlepart.to_file(geojson_buffer, driver='GeoJSON')
                geojson_buffer.seek(0)

                st.success("✅ GeoJSON created successfully!")

                # Format file name
                download_file_name = file_name_input.strip()
                if not download_file_name.lower().endswith(".geojson"):
                    download_file_name += ".geojson"

                # Show download button only
                st.download_button(
                    label="⬇️ Download GeoJSON",
                    data=geojson_buffer,
                    file_name=download_file_name,
                    mime="application/geo+json"
                )

            except Exception as e:
                st.error(f"❌ Error processing file: {e}")
