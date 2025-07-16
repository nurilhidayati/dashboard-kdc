import streamlit as st
import osmnx as ox
import geopandas as gpd
import io

st.title("🗺️ Restricted Area & Road Downloader")

# 👉 Input nama wilayah (berlaku global untuk semua tombol)
place_name = st.text_input("Enter a place name", value="Palembang, Indonesia")

# Fungsi: Download area terbatas (Polygon)
def download_restricted_areas(place):
    tags = {
        "landuse": ["military", "industrial", "commercial", "government", "reservoir",
                    "protected_area", "forest", "cemetery", "landfill"],
        "access": ["private", "customers", "permit", "military", "no"],
        "military": True,
        "building": ["government", "warehouse", "military", "university"],
        "barrier": ["fence", "wall", "gates", "bollard"],
        "amenity": ["school", "college", "university", "police", "hospital", "kindergarten"],
        "leisure": ["golf_course"],
        "aeroway": ["airport"],
        "tourism": ["forest"]
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
        "access": ["private", "no", "military", "customers", "permit"],
        "highway": ["service", "track", "motorway", "road", "motorway_link", "residential"],
        "service": True,
        "barrier": ["gate", "fence", "bollard"],
        "military": True,
        "landuse": ["military", "industrial", "government"]
    }
    gdf = ox.features.features_from_place(place, tags=tags)
    gdf = gdf[gdf.geometry.type.isin(["LineString", "MultiLineString"])]
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON")
    buffer.seek(0)
    return gdf, buffer

# --- Tombol 1: Area ---
if st.button("🔍 Download Restricted Areas (GeoJSON)"):
    try:
        st.info("Fetching restricted areas...")
        gdf_area, buffer_area = download_restricted_areas(place_name)
        st.success(f"✅ {len(gdf_area)} restricted areas found")
        st.download_button("⬇️ Download Areas", buffer_area, "restricted_areas.geojson", "application/geo+json")
        # Centroid map
        gdf_area = gdf_area.to_crs(epsg=4326)
        gdf_area["lon"] = gdf_area.geometry.centroid.x
        gdf_area["lat"] = gdf_area.geometry.centroid.y
        st.map(gdf_area[["lat", "lon"]])
    except Exception as e:
        st.error(f"❌ Error: {e}")

# --- Tombol 2: Road ---
if st.button("🚧 Download Restricted Roads (GeoJSON)"):
    try:
        st.info("Fetching restricted roads...")
        gdf_roads, buffer_roads = download_restricted_roads(place_name)
        st.success(f"✅ {len(gdf_roads)} restricted roads found")
        st.download_button("⬇️ Download Roads", buffer_roads, "restricted_roads.geojson", "application/geo+json")
        # Centroid map
        gdf_roads = gdf_roads.to_crs(epsg=4326)
        gdf_roads["lon"] = gdf_roads.geometry.centroid.x
        gdf_roads["lat"] = gdf_roads.geometry.centroid.y
        st.map(gdf_roads[["lat", "lon"]])
    except Exception as e:
        st.error(f"❌ Error: {e}")
