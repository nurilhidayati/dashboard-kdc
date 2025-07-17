import streamlit as st
import geopandas as gpd
from shapely.geometry import MultiLineString
import json
from io import BytesIO

def merge_linestrings(geojson_files):
    all_lines = []

    for uploaded_file in geojson_files:
        gdf = gpd.read_file(uploaded_file)
        
        # Filter only LineString or MultiLineString
        gdf = gdf[gdf.geometry.type.isin(['LineString', 'MultiLineString'])]
        
        for geom in gdf.geometry:
            if geom.type == 'LineString':
                all_lines.append(geom)
            elif geom.type == 'MultiLineString':
                all_lines.extend(geom.geoms)

    merged = MultiLineString(all_lines)
    merged_gdf = gpd.GeoDataFrame(geometry=[merged], crs="EPSG:4326")
    return merged_gdf

# Streamlit UI
st.title("🧵 Merge GeoJSON LineStrings")

uploaded_files = st.file_uploader(
    "📤 Upload one or more GeoJSON files with LineStrings", 
    type=["geojson"], 
    accept_multiple_files=True
)

if uploaded_files:
    if st.button("🔗 Merge LineStrings"):
        with st.spinner("Merging..."):
            try:
                merged_gdf = merge_linestrings(uploaded_files)
                st.success("✅ Successfully merged LineStrings!")

                st.map(merged_gdf)

                # Convert to GeoJSON string
                geojson_str = merged_gdf.to_json()
                geojson_bytes = BytesIO(geojson_str.encode("utf-8"))

                st.download_button(
                    label="📥 Download Merged GeoJSON",
                    data=geojson_bytes,
                    file_name="merged_lines.geojson",
                    mime="application/geo+json"
                )

            except Exception as e:
                st.error(f"❌ Error during merging: {e}")
