import streamlit as st
import geopandas as gpd
from shapely.geometry import MultiLineString
from io import BytesIO

# Merge function
def merge_linestrings(geojson_files):
    all_lines = []

    for uploaded_file in geojson_files:
        try:
            gdf = gpd.read_file(uploaded_file)

            # Filter LineString or MultiLineString
            gdf = gdf[gdf.geometry.type.isin(['LineString', 'MultiLineString'])]

            for geom in gdf.geometry:
                if geom.type == 'LineString':
                    all_lines.append(geom)
                elif geom.type == 'MultiLineString':
                    all_lines.extend(geom.geoms)

        except Exception as e:
            st.error(f"❌ Failed to read {uploaded_file.name}: {e}")

    if not all_lines:
        return None

    merged = MultiLineString(all_lines)
    merged_gdf = gpd.GeoDataFrame(geometry=[merged], crs="EPSG:4326")
    return merged_gdf

# UI
st.set_page_config(page_title="Merge GeoJSON LineStrings")
st.title("🔗 Merge GeoJSON LineStrings")

uploaded_files = st.file_uploader(
    "📤 Upload one or more GeoJSON files (LineString or MultiLineString)",
    type=["geojson"],
    accept_multiple_files=True
)

file_name_input = st.text_input("📝 Output filename (without .geojson):", value="merged_lines")

if uploaded_files and st.button("🔄 Merge Now"):
    with st.spinner("🔄 Processing..."):
        merged_gdf = merge_linestrings(uploaded_files)

        if merged_gdf is None or merged_gdf.empty:
            st.warning("⚠️ No valid LineStrings found.")
        else:
            st.success("✅ Merge completed!")

            # Convert to GeoJSON string
            geojson_str = merged_gdf.to_json()
            geojson_bytes = BytesIO(geojson_str.encode("utf-8"))

            final_name = file_name_input.strip() or "merged_lines"
            if not final_name.lower().endswith(".geojson"):
                final_name += ".geojson"

            # Download button only
            st.download_button(
                label="📥 Download Merged GeoJSON",
                data=geojson_bytes,
                file_name=final_name,
                mime="application/geo+json"
            )
