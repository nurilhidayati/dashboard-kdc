import streamlit as st
import osmnx as ox
import geopandas as gpd
import json
import io
import os
from shapely.geometry import shape

st.set_page_config(page_title="🔍 Download Area & Road", layout="wide")
st.title("📦 Download Restricted Area and Road from Boundary")

# File kabupaten dan provinsi
kab_file = "pages/batas_admin_kabupaten.geojson"
prov_file = "pages/batas_admin_provinsi.geojson"

# Load GeoJSON
kab_geojson, prov_geojson = None, None

if os.path.exists(kab_file):
    with open(kab_file, "r", encoding="utf-8") as f:
        kab_geojson = json.load(f)
else:
    st.error("❌ File 'batas_admin_kabupaten.geojson' tidak ditemukan")

if os.path.exists(prov_file):
    with open(prov_file, "r", encoding="utf-8") as f:
        prov_geojson = json.load(f)
else:
    st.error("❌ File 'batas_admin_provinsi.geojson' tidak ditemukan")

# Inisialisasi session_state
for key in ["selected_kabupaten", "selected_provinsi", "has_searched", "geojson_result",
            "gdf_area", "buffer_area", "show_area_download",
            "gdf_road", "buffer_road", "show_road_download"]:
    if key not in st.session_state:
        st.session_state[key] = None if key not in ["has_searched", "show_area_download", "show_road_download"] else False

# === Dropdown dan Tombol Cari ===
col1, col2, col3 = st.columns([5, 5, 1.5])

with col1:
    selected_kabupaten = None
    if kab_geojson:
        kabupaten_list = sorted({f["properties"].get("WADMKK") for f in kab_geojson["features"] if f["properties"].get("WADMKK")})
        selected_kabupaten = st.selectbox("🏙️ Select Regency:", ["-- Select Regency --"] + kabupaten_list)

with col2:
    selected_provinsi = None
    if prov_geojson:
        provinsi_list = sorted({f["properties"].get("PROVINSI") for f in prov_geojson["features"] if f["properties"].get("PROVINSI")})
        selected_provinsi = st.selectbox("🏞️ Select Province:", ["-- Select Province --"] + provinsi_list)

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 Search"):
        if selected_kabupaten and selected_kabupaten != "-- Select Regency --":
            st.session_state.selected_kabupaten = selected_kabupaten
            st.session_state.selected_provinsi = None
            st.session_state.has_searched = True
        elif selected_provinsi and selected_provinsi != "-- Select Province --":
            st.session_state.selected_provinsi = selected_provinsi
            st.session_state.selected_kabupaten = None
            st.session_state.has_searched = True

# Proses hasil pencarian
if st.session_state.has_searched:
    selected_geojson = None
    layer_name = ""

    if st.session_state.selected_kabupaten:
        filtered_kab = [
            f for f in kab_geojson["features"]
            if f["properties"].get("WADMKK") == st.session_state.selected_kabupaten
        ]
        selected_geojson = {"type": "FeatureCollection", "features": filtered_kab}
        layer_name = st.session_state.selected_kabupaten

    elif st.session_state.selected_provinsi:
        filtered_prov = [
            f for f in prov_geojson["features"]
            if f["properties"].get("PROVINSI") == st.session_state.selected_provinsi
        ]
        selected_geojson = {"type": "FeatureCollection", "features": filtered_prov}
        layer_name = st.session_state.selected_provinsi

    st.session_state.geojson_result = selected_geojson

# Fungsi: Download area terbatas
def download_restricted_areas(polygon):
    tags = {
        "landuse": ["military", "industrial", "commercial", "government", "cemetery", "landfill"],
        "leisure": ["nature_reserve", "golf_course"],
        "boundary": ["protected_area"],
        "aeroway": ["aerodrome"],
        "building": ["military", "government", "warehouse", "university", "school", "hospital"],
        "amenity": ["school", "college", "university", "police", "hospital", "kindergarten"],
        "barrier": ["fence", "wall", "gate", "bollard"],
        "access": ["private", "customers", "permit", "military", "no"]
    }
    gdf = ox.features.features_from_polygon(polygon, tags=tags)
    gdf = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON", index=False)
    buffer.seek(0)
    return gdf, buffer

# Fungsi: Download jalan terbatas
def download_restricted_roads(polygon):
    tags = {
        "highway": ["service", "unclassified", "track"],
        "access": ["private", "customers", "permit", "military", "no"],
        "motorcycle": ["no", "private"],
        "service": ["driveway", "alley", "emergency_access"],
    }
    gdf = ox.features.features_from_polygon(polygon, tags=tags)
    gdf = gdf[gdf.geometry.geom_type.isin(["LineString", "MultiLineString"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON", index=False)
    buffer.seek(0)
    return gdf, buffer

# Input nama file output
st.subheader("💾 Download")
area_filename = st.text_input("Filename for restricted **area** (without .geojson)", value="restricted_area")
road_filename = st.text_input("Filename for restricted **road** (without .geojson)", value="restricted_road")

polygon_gdf = None
if st.session_state.geojson_result:
    polygon_gdf = gpd.GeoDataFrame.from_features(st.session_state.geojson_result["features"])
    polygon_gdf.set_crs("EPSG:4326", inplace=True)
    polygon = polygon_gdf.unary_union

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("📦 Download Restricted Areas"):
            if not area_filename.strip():
                st.warning("⚠️ Please enter a filename.")
            else:
                try:
                    st.info("Fetching restricted areas...")
                    gdf_area, buffer_area = download_restricted_areas(polygon)
                    st.session_state.gdf_area = gdf_area
                    st.session_state.buffer_area = buffer_area
                    st.session_state.show_area_download = True
                    st.success(f"✅ {len(gdf_area)} restricted areas found")
                except Exception as e:
                    st.error(f"❌ Failed to fetch areas: {e}")
                    st.session_state.show_area_download = False

    with col_b:
        if st.button("🚧 Download Restricted Roads"):
            if not road_filename.strip():
                st.warning("⚠️ Please enter a filename.")
            else:
                try:
                    st.info("Fetching restricted roads...")
                    gdf_road, buffer_road = download_restricted_roads(polygon)
                    st.session_state.gdf_road = gdf_road
                    st.session_state.buffer_road = buffer_road
                    st.session_state.show_road_download = True
                    st.success(f"✅ {len(gdf_road)} restricted roads found")
                except Exception as e:
                    st.error(f"❌ Failed to fetch roads: {e}")
                    st.session_state.show_road_download = False

    # Tampilkan tombol download jika data tersedia
    if st.session_state.show_area_download and st.session_state.buffer_area:
        st.download_button("⬇️ Download Area GeoJSON", st.session_state.buffer_area,
                           f"{area_filename}.geojson", "application/geo+json")

    if st.session_state.show_road_download and st.session_state.buffer_road:
        st.download_button("⬇️ Download Road GeoJSON", st.session_state.buffer_road,
                           f"{road_filename}.geojson", "application/geo+json")
