import streamlit as st
import osmnx as ox
import geopandas as gpd
import io

st.title("Download Restricted Area and Restricted Road")

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
    gdf = gdf[gdf.geometry.geom_type.isin(["Polygon", "MultiPolygon"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON", index=False)  # Hindari warning fitur ID
    buffer.seek(0)
    return gdf, buffer

# Fungsi: Download jalan terbatas (LineString)
def download_restricted_roads(place):
    tags = {
        "highway": ["service", "unclassified", "track"],
        "access": ["private", "customers", "permit", "military", "no"],
        "motorcycle": ["no", "private"],
        "service": ["driveway", "alley", "emergency_access"],
    }

    gdf = ox.features.features_from_place(place, tags=tags)
    gdf = gdf[gdf.geometry.geom_type.isin(["LineString", "MultiLineString"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON", index=False)  # Hindari warning fitur ID
    buffer.seek(0)
    return gdf, buffer

# 👉 Input nama file output
area_filename = st.text_input("Filename for area (without .geojson)", value="")

# --- Tombol 1: Area ---
if st.button("🔍 Download Restricted Areas (GeoJSON)"):
    if not place_name.strip():
        st.warning("⚠️ Please enter a place name first.")
    elif not area_filename.strip():
        st.warning("⚠️ Please enter a filename for the area.")
    else:
        try:
            st.info("Fetching restricted areas...")
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

if st.session_state.show_area_download and st.session_state.buffer_area:
    st.download_button("⬇️ Download Areas", st.session_state.buffer_area,
                       f"{area_filename}.geojson", "application/geo+json")

# Filename untuk jalan
road_filename = st.text_input("Filename for roads (without .geojson)", value="")

# --- Tombol 2: Road ---
if st.button("🚧 Download Restricted Roads (GeoJSON)"):
    if not place_name.strip():
        st.warning("⚠️ Please enter a place name first.")
    elif not road_filename.strip():
        st.warning("⚠️ Please enter a filename for the roads.")
    else:
        try:
            st.info("Fetching restricted roads...")
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

if st.session_state.show_road_download and st.session_state.buffer_road:
    st.download_button("⬇️ Download Roads", st.session_state.buffer_road,
                       f"{road_filename}.geojson", "application/geo+json")

# Footer
st.markdown(
    """
    <hr style="margin-top: 2rem; margin-bottom: 1rem;">
    <div style='text-align: center; color: grey; font-size: 0.9rem;'>
        © 2025 ID Karta IoT Team
    </div>
    """,
    unsafe_allow_html=True
)
