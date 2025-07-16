import streamlit as st
import osmnx as ox
import geopandas as gpd
import io

st.title("🚫 Restricted Area Downloader (OSM Data)")

place_name = st.text_input("Enter a place name (e.g., Palembang, Indonesia)", value="Palembang, Indonesia")

tags = {
    "landuse": [
        "military", "industrial", "commercial", "government", "reservoir",
        "protected_area", "forest", "cemetery", "landfill"
    ],
    "access": [
        "private", "customers", "permit", "military", "no"
    ],
    "military": True,
    "building": [
        "government", "warehouse", "military", "university"
    ],
    "barrier": [
        "fence", "wall", "gates", "bollard"
    ],
    "amenity": [
        "school", "college", "university", "police", "hospital", "kindergarten"
    ],
    "leisure": [
        "golf_course"
    ],
    "aeroway": [
        "airport"
    ],
    "tourism": [
        "forest"
    ]
}

if st.button("🔍 Search & Download GeoJSON"):
    try:
        st.info("📦 Downloading data from OpenStreetMap...")
        gdf = ox.features.features_from_place(place_name, tags=tags)

        # Keep only polygons
        gdf = gdf[gdf.geometry.type.isin(["Polygon", "MultiPolygon"])]

        # Save to GeoJSON in memory
        buffer = io.BytesIO()
        gdf.to_file(buffer, driver="GeoJSON")
        buffer.seek(0)

        # Add lat/lon for mapping
        gdf = gdf.to_crs(epsg=4326)
        gdf["lon"] = gdf.geometry.centroid.x
        gdf["lat"] = gdf.geometry.centroid.y

        st.success(f"✅ Found {len(gdf)} features in {place_name}")

        # Download button
        st.download_button(
            label="⬇️ Download GeoJSON",
            data=buffer,
            file_name="restricted_areas.geojson",
            mime="application/geo+json"
        )

        # Show simple map
        st.map(gdf[["lat", "lon"]])

    except Exception as e:
        st.error(f"❌ Error: {e}")
