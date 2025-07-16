import streamlit as st

st.set_page_config(
    page_title="Analyst Gap Justification",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

st.title("🛠️ Analyst Gap Justification")

st.markdown("""
### 🔍 Overview

**Analyst Gap Justification** is a web-based geospatial tool built with Streamlit to support the identification and analysis of road segments near or inside restricted zones. This tool helps process coordinate data, visualize road geometry, retrieve restricted areas from OpenStreetMap, and conduct spatial intersection analysis.

---

### 🔄 Workflow

**✅ Step 1: Flatten Coordinates**  
Raw coordinate data is often grouped like this:  
`[[(104.75, -2.97), (104.76, -2.96)]]`  
This format stores multiple points in a single cell, making it hard to process and visualize.

**Why Flattening Is Needed:**  
- Converts grouped coordinates into one row per point  
- Prepares the data for creating line shapes (polylines)  
- Helps identify missing or incorrect points  

**Simple Analogy:**  
Imagine drawing a road. If all the points are jumbled together, it's hard to follow.  
But if each point is listed clearly, it becomes easier to connect them into a road.

To begin, upload a CSV file with grouped coordinates. The tool will flatten the data to make it ready for the next steps.

---

**✏️ Step 2: Convert to Polylines**  
The cleaned points are grouped by segment and transformed into continuous lines (polylines) that represent road paths. These are saved in GeoJSON format for further use.

---

**🌍 Step 3: Download Restricted Areas and Restricted Roads**  
The application retrieves restricted areas (e.g., military zones, industrial sites, government buildings) and restricted roads (e.g., private or limited-access) from OpenStreetMap in GeoJSON format.

---

**🚧 Step 4: Intersect with Restricted Zones**  
Uploaded road data is compared with restricted layers. Any road segments that intersect or fall within a specified buffer distance are extracted into a filtered result for analysis.

---

### 💬 Contact & Credits

📩 **Slack contact:** `nuril.hidayati`  
👥 **Project team:** ID Karta IoT Team – 2025  
🙏 **Special thanks to:** Qitfirul, Mahardi Pratomo, Annisa Dwi Maiikhsantiani, and Mochammad Fachri
""")
