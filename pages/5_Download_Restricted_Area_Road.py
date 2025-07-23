import streamlit as st
import osmnx as ox
import geopandas as gpd
import io
import time
from shapely.geometry import Polygon

st.title("Download Restricted Area and Road")

# 👉 Input nama wilayah
place_name = st.text_input("Enter a place name, e.g., Palembang, Indonesia", value="")

# Inisialisasi session state
for key in ["show_area_download", "buffer_area", "gdf_area", "show_road_download", "buffer_road", "gdf_road"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Helper: safe geocode
def safe_geocode(place, retries=3, delay=2):
    for i in range(retries):
        try:
            return ox.geocoder.geocode_to_gdf(place)
        except Exception as e:
            if i < retries - 1:
                time.sleep(delay)
            else:
                raise e

# Fungsi: Download area terbatas
def download_restricted_areas(place):
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

    gdf_place = safe_geocode(place)
    polygon = gdf_place.geometry.iloc[0]
    gdf = ox.features.features_from_polygon(polygon, tags=tags)
    gdf = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON", index=False)
    buffer.seek(0)
    return gdf, buffer

# Fungsi: Download jalan terbatas
def download_restricted_roads(place):
    tags = {
        "highway": ["service", "unclassified", "track"],
        "access": ["private", "customers", "permit", "military", "no"],
        "motorcycle": ["no", "private"],
        "service": ["driveway", "alley", "emergency_access"],
    }

    gdf_place = safe_geocode(place)
    polygon = gdf_place.geometry.iloc[0]
    gdf = ox.features.features_from_polygon(polygon, tags=tags)
    gdf = gdf[gdf.geometry.geom_type.isin(["LineString", "MultiLineString"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON", index=False)
    buffer.seek(0)
    return gdf, buffer

# 👉 Input nama file output
area_filename = st.text_input("Filename for area (without .geojson)", value="restricted_area")
road_filename = st.text_input("Filename for road (without .geojson)", value="restricted_road")

# --- Tombol Area ---
if st.button("🔍 Download Restricted Areas (GeoJSON)"):
    if not place_name.strip():
        st.warning("⚠️ Please enter a place name.")
    elif not area_filename.strip():
        st.warning("⚠️ Please enter a filename for the area.")
    else:
        try:
            st.info("Fetching restricted areas...")
            gdf_area, buffer_area = download_restricted_areas(place_name)
            st.session_state.gdf_area = gdf_area
            st.session_state.buffer_area = buffer_area
            st.session_state.show_area_download = True
            st.success(f"✅ {len(gdf_area)} restricted areas found")
        except Exception as e:
            st.error(f"❌ Geocoding failed: {e}")
            st.session_state.show_area_download = False

if st.session_state.show_area_download and st.session_state.buffer_area:
    st.download_button("⬇️ Download Areas", st.session_state.buffer_area,
                       f"{area_filename}.geojson", "application/geo+json")

# --- Tombol Jalan ---
if st.button("🚧 Download Restricted Roads (GeoJSON)"):
    if not place_name.strip():
        st.warning("⚠️ Please enter a place name.")
    elif not road_filename.strip():
        st.warning("⚠️ Please enter a filename for the roads.")
    else:
        try:
            st.info("Fetching restricted roads...")
            gdf_road, buffer_road = download_restricted_roads(place_name)
            st.session_state.gdf_road = gdf_road
            st.session_state.buffer_road = buffer_road
            st.session_state.show_road_download = True
            st.success(f"✅ {len(gdf_road)} restricted roads found")
        except Exception as e:
            st.error(f"❌ Geocoding failed: {e}")
            st.session_state.show_road_download = False

if st.session_state.show_road_download and st.session_state.buffer_road:
    st.download_button("⬇️ Download Roads", st.session_state.buffer_road,
                       f"{road_filename}.geojson", "application/geo+json")
