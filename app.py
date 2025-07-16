import streamlit as st

st.set_page_config(
    page_title="Analyst Gap Justification",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

st.title("🛠️ Analyst Gap Justification")

st.markdown("""
### 🔍 Overview

Analyst Gap Justification is a web-based geospatial tool built with Streamlit that facilitates the detection and analysis of gaps in infrastructure or planning, especially in relation to restricted zones. It provides a simple interface to convert raw coordinate data, visualize roads, download restricted areas from OpenStreetMap, and perform spatial analysis through intersection.
---

### 🔄 Workflow  

**✅ Step 1: Flatten Coordinates**  
Upload a CSV file containing grouped coordinate data. The application separates these into individual rows so that each point is clearly represented. This format prepares the data for conversion into line features in the next step.

**✏️ Step 2: Convert to Polylines**  
The cleaned coordinate points are grouped by segment and transformed into continuous line shapes (polylines) representing road paths. These are saved in GeoJSON format, which is suitable for mapping and further analysis.

**🌍 Step 3: Download Restricted Areas and Roads**  
Select a city or area of interest. The application retrieves data from OpenStreetMap, including restricted zones such as military compounds, industrial sites, or government buildings, as well as roads marked as private or limited access. The data is provided in GeoJSON format.


**🚧 Step 4: Intersect with Restricted Zones**  
Uploaded road data is compared against the restricted area layers. The analysis identifies any roads that intersect with or fall within a specified buffer distance of these zones. The result is a filtered dataset highlighting only those segments of interest.


💬 Contact & Credits

📩 Slack contact: nuril.hidayati

👥 Project team: ID Karta IoT Team – 2025

🙏 Special thanks to: Qitfirul, Mahardi Pratomo, Annisa Dwi Maiikhsantiani, and Mochammad Fachri
