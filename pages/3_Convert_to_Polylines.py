import streamlit as st
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import io

st.title("📍 CSV to LineString GeoJSON Converter")

uploaded_file = st.file_uploader("Upload your flattened CSV file", type=["csv"])

if uploaded_file:
    try:
        # Load uploaded CSV into pandas
        df = pd.read_csv(uploaded_file)

        # Group by segment_id to construct LineStrings
        lines = []
        metadata_rows = []

        for seg_id, group in df.groupby("segment_id"):
            coords = list(zip(group["x"], group["y"]))
            lines.append(LineString(coords))

            meta = group.iloc[0].copy()
            meta["coords"] = coords
            metadata_rows.append(meta)

        # Create GeoDataFrame
        gdf_roads = gpd.GeoDataFrame(metadata_rows, geometry=lines, crs="EPSG:4326")

        # Explode multipart geometries to singlepart
        gdf_singlepart = gdf_roads.explode(index_parts=False).reset_index(drop=True)

        # Add x and y for start point
        gdf_singlepart["x"] = gdf_singlepart.geometry.apply(lambda geom: geom.coords[0][0])
        gdf_singlepart["y"] = gdf_singlepart.geometry.apply(lambda geom: geom.coords[0][1])

        # Save to GeoJSON in memory
        geojson_buffer = io.BytesIO()
        gdf_singlepart.to_file(geojson_buffer, driver='GeoJSON')
        geojson_buffer.seek(0)

        # Success message
        st.success("✅ GeoJSON created successfully!")

        # Preview data
        st.dataframe(gdf_singlepart[["id", "segment_id", "x", "y"]].head())

        # Download button
        st.download_button(
            label="⬇️ Download GeoJSON",
            data=geojson_buffer,
            file_name="2024campaign_singlepart.geojson",
            mime="application/geo+json"
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
