import streamlit as st

st.set_page_config(
    page_title="Analyst Gap Justification",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

st.title("🛠️ Analyst Gap Justification")

st.markdown("""
### 🔍 Overview

**Analyst Gap Justification** is a web-based geospatial tool built with Streamlit to support the identification and analysis of road segments near or inside restricted zones. This tool allows users to process coordinate data, visualize road geometry, retrieve restricted areas from OpenStreetMap, and conduct spatial intersection analysis.

---

### 🔄 Workflow

**✅ Step 1: Flatten Coordinates**  
Upload a CSV file containing grouped coordinate data. The tool separates them into individual rows to ensure that each point is clearly structured for the next stage.

**✏️ Step 2: Convert to Polylines**  
Grouped coordinates are converted into continuous lines (polylines) that represent road segments. These are saved in GeoJSON format, ready for visualization or further analysis.

**🌍 Step 3: Download Restricted Areas and Roads**  
Select a region of interest. The application retrieves restricted area data (e.g., military, industrial, or government zones) and road segments marked with restricted access from OpenStreetMap, provided in GeoJSON format.

**🚧 Step 4: Intersect with Restricted Zones**  
Uploaded road data is compared against restricted layers. Roads that intersect or are located within a defined distance of these zones are extracted into a filtered dataset.

---

### 💬 Contact & Credits

📩 **Slack contact:** `nuril.hidayati`  
👥 **Project team:** ID Karta IoT Team – 2025  
🙏 **Special thanks to:** Qitfirul, Mahardi Pratomo, Annisa Dwi Maiikhsantiani, and Mochammad Fachri
""")
