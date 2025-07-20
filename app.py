import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import os

st.set_page_config(page_title="🛠️ RoadValidation App", layout="wide")
st.title("🛠️ RoadValidation App")

st.markdown("""
This app helps mapping teams validate road data against restricted zones using OpenStreetMap (OSM). Follow the workflow below.
""")

st.sidebar.title("📌 Navigation")
step = st.sidebar.radio("Select Step", [
    "1️⃣ Split Data by City Name",
    "2️⃣ Flatten Coordinates",
    "3️⃣ Convert to LineString",
    "4️⃣ Merge GeoJSON (Optional)",
    "5️⃣ Download Restricted Area Road",
    "6️⃣ Analyst Gap Justification"
])

# STEP 1
if step == "1️⃣ Split Data by City Name":
    st.header("✅ Step 1: Split Data by City Name")
    uploaded_file = st.file_uploader("📤 Upload your CSV file", type="csv")
    city_name = st.text_input("🏙️ Please Enter City Name (e.g., Jakarta)")
    download_option = st.radio("📎 Choose Download Option:", [
        "Download All in One File", 
        "Download in Batches (5000 rows each)"
    ])
    
    if uploaded_file and city_name:
        df = pd.read_csv(uploaded_file)
        filtered = df[df['grid_id'].str.split().str[1] == city_name]
        if download_option == "Download All in One File":
            st.download_button("⬇️ Download Filtered CSV", filtered.to_csv(index=False), file_name=f"{city_name}_all.csv")
        else:
            chunks = [filtered[i:i+5000] for i in range(0, len(filtered), 5000)]
            for idx, chunk in enumerate(chunks):
                st.download_button(f"⬇️ Download Chunk {idx+1}", chunk.to_csv(index=False), file_name=f"{city_name}_part{idx+1}.csv")
    elif uploaded_file:
        st.warning("Please enter a city name.")

# STEP 2
elif step == "2️⃣ Flatten Coordinates":
    st.header("✅ Step 2: Flatten Coordinates")
    uploaded_file = st.file_uploader("📂 Upload CSV file with road_coordinates", type="csv")
    output_name = st.text_input("📝 Enter output file name (without .csv):")
    
    if uploaded_file and output_name:
        df = pd.read_csv(uploaded_file)
        # Implement your flattening logic here
        st.info("📌 Flattening logic not yet implemented.")
    elif uploaded_file:
        st.warning("Please enter output file name.")

# STEP 3
elif step == "3️⃣ Convert to LineString":
    st.header("✅ Step 3: Convert CSV Points to GeoJSON LineString")
    uploaded_file = st.file_uploader("📤 Upload your flattened CSV file", type="csv")
    output_name = st.text_input("📝 Enter output file name (without .geojson):")
    
    if uploaded_file and output_name:
        df = pd.read_csv(uploaded_file)
        # Implement conversion logic here
        st.info("📌 LineString conversion logic not yet implemented.")
    elif uploaded_file:
        st.warning("Please enter output file name.")

# STEP 4
elif step == "4️⃣ Merge GeoJSON (Optional)":
    st.header("✅ Step 4: Merge GeoJSON LineStrings (Optional for Large Dataset)")
    uploaded_files = st.file_uploader("📤 Upload one or more GeoJSON files", type="geojson", accept_multiple_files=True)
    output_name = st.text_input("📝 Output filename (without .geojson):")
    
    if uploaded_files and output_name:
        gdfs = [gpd.read_file(f) for f in uploaded_files]
        merged = pd.concat(gdfs).reset_index(drop=True)
        geojson = merged.to_json()
        st.download_button("⬇️ Download Merged GeoJSON", geojson, file_name=f"{output_name}.geojson")
    elif uploaded_files:
        st.warning("Please enter output file name.")

# STEP 5
elif step == "5️⃣ Download Restricted Area Road":
    st.header("✅ Step 5: Download Restricted Area and Road from OSM")
    place_name = st.text_input("🌍 Enter a place name (e.g., Jakarta, Indonesia)")
    area_filename = st.text_input("📁 Filename for area (without .geojson):")
    road_filename = st.text_input("📁 Filename for roads (without .geojson):")

    if place_name and area_filename and road_filename:
        st.info("📌 OSM downloading logic not yet implemented.")
    elif place_name:
        st.warning("Please enter both filenames for area and road.")

# STEP 6
elif step == "6️⃣ Analyst Gap Justification":
    st.header("✅ Step 6: Analyst Gap Justification")
    
    road_geojson = st.file_uploader("📤 Upload Road GeoJSON", type="geojson")
    area_geojson = st.file_uploader("📤 Upload Restricted Area GeoJSON", type="geojson")
    restricted_road_geojson = st.file_uploader("📤 Upload Restricted Road GeoJSON", type="geojson")
    output_name = st.text_input("📝 Output filename (without .geojson):")
    
    if road_geojson and area_geojson and restricted_road_geojson and output_name:
        gdf_road = gpd.read_file(road_geojson)
        gdf_area = gpd.read_file(area_geojson)
        gdf_restrict = gpd.read_file(restricted_road_geojson)

        # Sample logic: spatial join (for demo purposes)
        joined = gpd.sjoin(gdf_road, gdf_area, predicate='intersects', how='inner')
        output = joined[['geometry']]
        geojson = output.to_json()
        st.download_button("⬇️ Download Validated GeoJSON", geojson, file_name=f"{output_name}.geojson")
    elif road_geojson or area_geojson or restricted_road_geojson:
        st.warning("Please upload all three required files and provide an output name.")
