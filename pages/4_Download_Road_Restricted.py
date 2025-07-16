import streamlit as st
import osmnx as ox
import geopandas as gpd
import io

def download_restricted_roads(place_name):
    """
    Download restricted roads for a given place from OSM.
    Returns: GeoDataFrame and buffer of GeoJSON
    """

    # Define OSM filter tags for restricted roads
    tags = {
        "access": ["private", "no", "military", "customers", "permit"],
        "highway": True,
        "service": True,
        "barrier": ["gate", "fence", "bollard"],
        "military": True,
        "landuse": ["military", "industrial", "government"]
    }

    # Query OSM data with OSMnx
    gdf = ox.features.features_from_place(place_name, tags=tags)

    # Filter only linestrings or multilinestrings
    gdf = gdf[gdf.geometry.type.isin(["LineString", "MultiLineString"])]

    # Save to in-memory GeoJSON
    buffer = io.BytesIO()
    gdf.to_file(buffer, driver="GeoJSON")
    buffer.seek(0)

    return gdf, buffer

if st.button("🚧 Download Road Restricted GeoJSON"):
    try:
        st.info("📦 Downloading restricted roads data...")
        gdf_roads, buffer_roads = download_restricted_roads(place_name)

        st.success(f"✅ Found {len(gdf_roads)} restricted road segments")

        st.download_button(
            label="⬇️ Download Road Restricted GeoJSON",
            data=buffer_roads,
            file_name="restricted_roads.geojson",
            mime="application/geo+json"
        )

        # Show map (centroid for simplicity)
        gdf_roads = gdf_roads.to_crs(epsg=4326)
        gdf_roads["lon"] = gdf_roads.geometry.centroid.x
        gdf_roads["lat"] = gdf_roads.geometry.centroid.y
        st.map(gdf_roads[["lat", "lon"]])

    except Exception as e:
        st.error(f"❌ Error: {e}")
