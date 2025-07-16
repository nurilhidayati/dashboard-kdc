import streamlit as st
import geopandas as gpd
import io

st.title("🛣️ Select Roads Intersecting Restricted Areas")

def select_restricted_roads(gdf_roads, gdf_polygons, gdf_lines=None, distance_meters=100.0):
    # Convert to projected CRS (UTM) for distance calculation
    if gdf_roads.crs.is_geographic:
        utm_crs = gdf_roads.estimate_utm_crs()
        gdf_roads = gdf_roads.to_crs(utm_crs)
        gdf_polygons = gdf_polygons.to_crs(utm_crs)
        if gdf_lines is not None:
            gdf_lines = gdf_lines.to_crs(utm_crs)

    # Buffer polygon layer
    buffered_polygons = gdf_polygons.buffer(distance_meters)
    buffered_polygons_gdf = gpd.GeoDataFrame(geometry=buffered_polygons, crs=gdf_polygons.crs)

    # Combine with line (if provided)
    if gdf_lines is not None:
        combined_geometry = buffered_polygons_gdf.geometry.append(gdf_lines.geometry)
        all_combined = gpd.GeoDataFrame(geometry=combined_geometry, crs=buffered_polygons_gdf.crs)
    else:
        all_combined = buffered_polygons_gdf

    # Spatial join
    selected = gpd.sjoin(gdf_roads, all_combined, how="inner", predicate="intersects")

    # Drop duplicates & convert back to WGS84
    selected = selected.drop_duplicates(subset=gdf_roads.columns)
    return selected.to_crs("EPSG:4326")

# Upload UI
uploaded_roads = st.file_uploader("📤 Upload Road GeoJSON", type=["geojson"])
uploaded_polygons = st.file_uploader("📤 Upload Restricted Area (Polygon GeoJSON)", type=["geojson"])
uploaded_lines = st.file_uploader("📤 Optional: Upload Barrier Lines (GeoJSON)", type=["geojson"])
distance = st.slider("📏 Distance buffer for polygons (meters)", 10, 1000, 100, step=10)

if uploaded_roads and uploaded_polygons:
    try:
        gdf_roads = gpd.read_file(uploaded_roads)
        gdf_polygons = gpd.read_file(uploaded_polygons)
        gdf_lines = gpd.read_file(uploaded_lines) if uploaded_lines else None

        st.info("🔍 Processing intersections...")
        selected_roads = select_restricted_roads(gdf_roads, gdf_polygons, gdf_lines, distance)

        st.success(f"✅ Found {len(selected_roads)} intersecting roads.")

        # Add for mapping
        selected_roads["lon"] = selected_roads.geometry.centroid.x
        selected_roads["lat"] = selected_roads.geometry.centroid.y
        st.map(selected_roads[["lat", "lon"]])

        # Download
        buffer = io.BytesIO()
        selected_roads.to_file(buffer, driver="GeoJSON")
        buffer.seek(0)

        st.download_button(
            "⬇️ Download Intersected Roads",
            buffer,
            file_name="intersected_roads.geojson",
            mime="application/geo+json"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
