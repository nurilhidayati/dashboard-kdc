import streamlit as st
import osmnx as ox
import geopandas as gpd
import io
from shapely.geometry import box

st.title("Download Restricted Area and Restricted Road (Offline Mode)")

# Input manual koordinat bounding box
st.markdown("### 📍 Define bounding box")
minx = st.number_input("Min Longitude", value=104.70)
miny = st.number_input("Min Latitude", value=-3.05)
maxx = st.number_input("Max Longitude", value=104.83)
maxy = st.number_input("Max Latitude", value=-2.90)

bbox_polygon = box(minx, miny, maxx, maxy)

# Inisialisasi session state
for key in ["show_area_download", "buffer_area", "gdf_area", "show_road_download", "buffer_road", "gdf_road"]:
    if key not in st.session_state:
        st.session_state[key] = None

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

# Input nama file
area_filename = st.text_input("Filename for area (without .geojson)", value="restricted_area")
road_filename = st.text_input("Filename for road (without .geojson)", value="restricted_road")

# Tombol 1
if st.button("🔍 Download Restricted Areas (GeoJSON)"):
    try:
        st.info("Fetching restricted areas...")
        gdf_area, buffer_area = download_restricted_areas(bbox_polygon)
        st.session_state.gdf_area = gdf_area
        st.session_state.buffer_area = buffer_area
        st.session_state.show_area_download = True
        st.success(f"✅ {len(gdf_area)} restricted areas found")
    except Exception as e:
        st.error(f"❌ Error: {e}")

if st.session_state.show_area_download and st.session_state.buffer_area:
    st.download_button("⬇️ Download Areas", st.session_state.buffer_area,
                       f"{area_filename}.geojson", "application/geo+json")

# Tombol 2
if st.button("🚧 Download Restricted Roads (GeoJSON)"):
    try:
        st.info("Fetching restricted roads...")
        gdf_road, buffer_road = download_restricted_roads(bbox_polygon)
        st.session_state.gdf_road = gdf_road
        st.session_state.buffer_road = buffer_road
        st.session_state.show_road_download = True
        st.success(f"✅ {len(gdf_road)} restricted roads found")
    except Exception as e:
        st.error(f"❌ Error: {e}")

if st.session_state.show_road_download and st.session_state.buffer_road:
    st.download_button("⬇️ Download Roads", st.session_state.buffer_road,
                       f"{road_filename}.geojson", "application/geo+json")
