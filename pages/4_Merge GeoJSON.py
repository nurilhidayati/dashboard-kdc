import streamlit as st
import geopandas as gpd
from shapely.geometry import MultiLineString
from io import BytesIO

# Merge function
def merge_linestrings(geojson_files):
    all_lines = []

    for uploaded_file in geojson_files:
        try:
            gdf = gpd.read_file(uploaded_file)

            # Filter LineString or MultiLineString
            gdf = gdf[gdf.geometry.type.isin(['LineString', 'MultiLineString'])]

            for geom in gdf.geometry:
                if geom.type == 'LineString':
                    all_lines.append(geom)
                elif geom.type == 'MultiLineString':
                    all_lines.extend(geom.geoms)

        except Exception as e:
            st.error(f"❌ Failed to read {uploaded_file.name}: {e}")

    if not all_lines:
        return None

    merged = MultiLineString(all_lines)
    merged_gdf = gpd.GeoDataFrame(geometry=[merged], crs="EPSG:4326")
    return merged_gdf

# UI
st.set_page_config(page_title="Merge GeoJSON LineStrings")
st.title("Merge GeoJSON LineStrings (Optional)")

# Init session state
if "geojson_bytes" not in st.session_state:
    st.session_state.geojson_bytes = None
if "final_name" not in st.session_state:
    st.session_state.final_name = ""

uploaded_files = st.file_uploader(
    "📤 Upload one or more GeoJSON files",
    type=["geojson"],
    accept_multiple_files=True,
    key="uploader"
)

file_name_input = st.text_input("📝 Output filename (without .geojson):", value="")

if st.button("🔄 Merge Now"):
    # Clear previous result first
    st.session_state.geojson_bytes = None
    st.session_state.final_name = ""

    if not uploaded_files:
        st.warning("⚠️ Please upload at least one file first.")
    elif not file_name_input.strip():
        st.warning("⚠️ Please enter an output filename.")
    else:
        with st.spinner("🔄 Processing..."):
            merged_gdf = merge_linestrings(uploaded_files)

            if merged_gdf is None or merged_gdf.empty:
                st.warning("⚠️ No valid LineStrings found.")
            else:
                st.success("✅ Merge completed!")

                geojson_str = merged_gdf.to_json()
                st.session_state.geojson_bytes = BytesIO(geojson_str.encode("utf-8"))

                final_name = file_name_input.strip()
                if not final_name.lower().endswith(".geojson"):
                    final_name += ".geojson"
                st.session_state.final_name = final_name

# Show download button only when available
if st.session_state.geojson_bytes:
    st.download_button(
        label="📥 Download Merged GeoJSON",
        data=st.session_state.geojson_bytes,
        file_name=st.session_state.final_name,
        mime="application/geo+json"
    )


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
