import streamlit as st
import osmnx as ox
import geopandas as gpd
import io

st.title("🗺️ Download Restricted Area and Road")

# 👉 Input nama wilayah
place_name = st.text_input("Enter a place name, ex: Jakarta, Indonesia", value="")

# Inisialisasi session state
for key in ["show_area_download", "buffer_area", "gdf_area", "show_road_download", "buffer_road", "gdf_road"]:
    if key not in st.session_state:
        st.session_state[key] = None

# Fungsi: Download area terbatas (Polygon)
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

    gdf = ox.features.features_from_place(place, tags=tags)
    gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON")
    buffer.seek(0)
    return gdf, buffer

# Fungsi: Download jalan terbatas (LineString)
def download_restricted_roads(place):
    tags = {
        "highway": ["service", "unclassified", "residential", "track"],
        "access": ["private", "customers", "permit", "military", "no"],
        "motor_vehicle": ["private", "no"],
        "motorcar": ["private", "no"],
        "service": ["driveway", "alley", "emergency_access"],
    }

    gdf = ox.features.features_from_place(place, tags=tags)
    gdf = gdf[gdf.geometry.type.isin(["LineString", "MultiLineString"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON")
    buffer.seek(0)
    return gdf, buffer

# 👉 Input nama file output
area_filename = st.text_input("Filename for area (without .geojson)", value="restricted_areas")

# --- Tombol 1: Area ---
if st.button("🔍 Download Restricted Areas (GeoJSON)"):
    if not place_name.strip():
        st.warning("⚠️ Please enter a place name first.")
    elif not area_filename.strip():
        st.warning("⚠️ Please enter a filename for the area.")
    else:
        try:
            st.info("Fetching restricted areas...")
            # Reset data sebelumnya
            st.session_state.gdf_area = None
            st.session_state.buffer_area = None
            st.session_state.show_area_download = False

            gdf_area, buffer_area = download_restricted_areas(place_name)
            st.session_state.gdf_area = gdf_area
            st.session_state.buffer_area = buffer_area
            st.session_state.show_area_download = True
            st.success(f"✅ {len(gdf_area)} restricted areas found")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.show_area_download = False

# Tampilkan tombol download jika tersedia
if st.session_state.show_area_download and st.session_state.buffer_area:
    st.download_button("⬇️ Download Areas", st.session_state.buffer_area,
                       f"{area_filename}.geojson", "application/geo+json")


road_filename = st.text_input("Filename for roads (without .geojson)", value="restricted_roads")

# --- Tombol 2: Road ---
if st.button("🚧 Download Restricted Roads (GeoJSON)"):
    if not place_name.strip():
        st.warning("⚠️ Please enter a place name first.")
    elif not road_filename.strip():
        st.warning("⚠️ Please enter a filename for the roads.")
    else:
        try:
            st.info("Fetching restricted roads...")
            # Reset data sebelumnya
            st.session_state.gdf_road = None
            st.session_state.buffer_road = None
            st.session_state.show_road_download = False

            gdf_road, buffer_road = download_restricted_roads(place_name)
            st.session_state.gdf_road = gdf_road
            st.session_state.buffer_road = buffer_road
            st.session_state.show_road_download = True
            st.success(f"✅ {len(gdf_road)} restricted roads found")
        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.show_road_download = False

# Tampilkan tombol download jika tersedia
if st.session_state.show_road_download and st.session_state.buffer_road:
    st.download_button("⬇️ Download Roads", st.session_state.buffer_road,
                       f"{road_filename}.geojson", "application/geo+json")
