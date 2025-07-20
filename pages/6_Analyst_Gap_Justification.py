import streamlit as st
import geopandas as gpd
import pandas as pd
import io

st.title("Analyst Gap Justification")

# Fungsi utama
def select_restricted_roads(gdf_roads, gdf_polygons, gdf_lines, distance_meters=100.0):
    if gdf_roads.crs.is_geographic:
        utm_crs = gdf_roads.estimate_utm_crs()
        gdf_roads = gdf_roads.to_crs(utm_crs)
        gdf_polygons = gdf_polygons.to_crs(utm_crs)
        gdf_lines = gdf_lines.to_crs(utm_crs)

    buffered_polygons = gdf_polygons.buffer(distance_meters)
    buffered_polygons_gdf = gpd.GeoDataFrame(geometry=buffered_polygons, crs=gdf_polygons.crs)

    combined_geometry = pd.concat([buffered_polygons_gdf.geometry, gdf_lines.geometry], ignore_index=True)
    all_combined = gpd.GeoDataFrame(geometry=combined_geometry, crs=buffered_polygons_gdf.crs)

    selected = gpd.sjoin(gdf_roads, all_combined, how="inner", predicate="intersects")
    selected = selected.drop_duplicates(subset=gdf_roads.columns)
    return selected.to_crs("EPSG:4326")

# Upload UI
uploaded_roads = st.file_uploader("📤 Upload Road GeoJSON", type=["geojson"])
uploaded_polygons = st.file_uploader("📤 Upload Restricted Area (Polygon GeoJSON)", type=["geojson"])
uploaded_lines = st.file_uploader("📤 Upload Restricted Road (Linestring GeoJSON)", type=["geojson"])

# Inisialisasi state
if "selected_roads" not in st.session_state:
    st.session_state.selected_roads = None

# Input nama file output
output_filename = st.text_input("📝 Output filename (tanpa ekstensi .geojson)")

# Tombol selalu muncul
process_clicked = st.button("▶️ Process")

# Jika tombol diklik, cek kondisi upload
if process_clicked:
    missing = []
    if not uploaded_roads:
        missing.append("📂 Road file")
    if not uploaded_polygons:
        missing.append("📂 Restricted Area file")
    if not uploaded_lines:
        missing.append("📂 Restricted Road file")

    if missing:
        for msg in missing:
            st.warning(f"⚠️ {msg} is not yet uploaded.")
    else:
        try:
            gdf_roads = gpd.read_file(uploaded_roads)
            gdf_polygons = gpd.read_file(uploaded_polygons)
            gdf_lines = gpd.read_file(uploaded_lines)

            selected = select_restricted_roads(gdf_roads, gdf_polygons, gdf_lines)
            st.session_state.selected_roads = selected
            st.success(f"✅ Found {len(selected)} intersecting roads.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.selected_roads = None

# Tampilkan tombol download jika data tersedia dan filename valid
if st.session_state.selected_roads is not None:
    selected = st.session_state.selected_roads.copy()

    if output_filename.strip() == "":
        st.warning("⚠️ Kindly provide an output filename before downloading")
    else:
        if not output_filename.lower().endswith(".geojson"):
            output_filename += ".geojson"

        buffer = io.BytesIO()
        selected.to_file(buffer, driver="GeoJSON")
        buffer.seek(0)

        st.download_button(
            "⬇️ Download Intersected Roads",
            buffer,
            file_name=output_filename,
            mime="application/geo+json"
        )
