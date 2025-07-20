import streamlit as st
import osmnx as ox
import geopandas as gpd
import io

st.title("🗺️ Download Restricted Area and Road")


# 👉 Input nama wilayah
place_name = st.text_input("Enter a place name", value="")

# Inisialisasi session state untuk area
if "show_area_download" not in st.session_state:
    st.session_state.show_area_download = False
if "buffer_area" not in st.session_state:
    st.session_state.buffer_area = None
if "gdf_area" not in st.session_state:
    st.session_state.gdf_area = None

# Inisialisasi session state untuk roads
if "show_road_download" not in st.session_state:
    st.session_state.show_road_download = False
if "buffer_road" not in st.session_state:
    st.session_state.buffer_road = None
if "gdf_road" not in st.session_state:
    st.session_state.gdf_road = None

# Fungsi: Download area terbatas (Polygon)
def download_restricted_areas(place):
    tags = {
    # Area penggunaan lahan yang sering terbatas aksesnya
    "landuse": [
        "military", "industrial", "commercial", "government", 
        "cemetery", "landfill"
    ],
    
    # Area dilindungi dan tempat umum yang dibatasi
    "leisure": ["nature_reserve", "golf_course"],
    "boundary": ["protected_area"],
    "aeroway": ["aerodrome"],

    # Bangunan penting dengan potensi akses terbatas
    "building": ["military", "government", "warehouse", "university", "school", "hospital"],

    # Fasilitas umum dengan potensi pembatasan akses
    "amenity": ["school", "college", "university", "police", "hospital", "kindergarten"],
    
    # Pembatas fisik (opsional, bisa diambil terpisah)
    "barrier": ["fence", "wall", "gate", "bollard"],
    
    # Pembatasan akses eksplisit
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
    "highway": ["service", "unclassified", "residential", "track"],  # semua tipe jalan kecil
    "access": ["private", "customers", "permit", "military", "no"],  # batasan akses
    "motor_vehicle": ["private", "no"],  # pembatas kendaraan bermotor
    "motorcar": ["private", "no"],
    "service": ["driveway", "alley", "emergency_access"],  # biasanya restricted
    }
    gdf = ox.features.features_from_place(place, tags=tags)
    gdf = gdf[gdf.geometry.type.isin(["LineString", "MultiLineString"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON")
    buffer.seek(0)
    return gdf, buffer

# --- Tombol 1: Toggle Area Download ---
if st.button("🔍 Download Restricted Areas (GeoJSON)"):
    if not place_name.strip():
        st.warning("⚠️ Please enter a place name first.")
    else:
        if st.session_state.show_area_download:
            # Hide download button
            st.session_state.show_area_download = False
            st.session_state.buffer_area = None
            st.session_state.gdf_area = None
        else:
            try:
                st.info("Fetching restricted areas...")
                gdf_area, buffer_area = download_restricted_areas(place_name)
                st.session_state.gdf_area = gdf_area
                st.session_state.buffer_area = buffer_area
                st.session_state.show_area_download = True
                st.success(f"✅ {len(gdf_area)} restricted areas found")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.session_state.show_area_download = False

# Show download button if ready
if st.session_state.show_area_download and st.session_state.buffer_area:
    st.download_button("⬇️ Download Areas", st.session_state.buffer_area,
                       "restricted_areas.geojson", "application/geo+json")

# --- Tombol 2: Toggle Road Download ---
if st.button("🚧 Download Restricted Roads (GeoJSON)"):
    if not place_name.strip():
        st.warning("⚠️ Please enter a place name first.")
    else:
        if st.session_state.show_road_download:
            # Hide download button
            st.session_state.show_road_download = False
            st.session_state.buffer_road = None
            st.session_state.gdf_road = None
        else:
            try:
                st.info("Fetching restricted roads...")
                gdf_road, buffer_road = download_restricted_roads(place_name)
                st.session_state.gdf_road = gdf_road
                st.session_state.buffer_road = buffer_road
                st.session_state.show_road_download = True
                st.success(f"✅ {len(gdf_road)} restricted roads found")
            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.session_state.show_road_download = False

# Show download button if ready
if st.session_state.show_road_download and st.session_state.buffer_road:
    st.download_button("⬇️ Download Roads", st.session_state.buffer_road,
                       "restricted_roads.geojson", "application/geo+json")
