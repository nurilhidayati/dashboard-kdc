import streamlit as st

st.set_page_config(
    page_title="GeoHash Toolbox",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

st.title("🛠️ Analyst Gap Justification")

st.markdown("""
### 📄 Overview  
This website is developed to support the analysis of **Gap Justification** in the context of spatial data processing and restricted area validation.

---

### 🔄 Workflow  

**1. Flattened Coordinates**  
`Process raw coordinate data into a normalized tabular structure.`

**2. Convert Data to Polyline**  
`Transform flattened coordinate sequences into geographic polyline features.`

**3. Download Area & Road Restricted**  
`Retrieve restricted zones and classified roads from OpenStreetMap.`

**4. Intersect Data**  
`Perform spatial intersection analysis between user-provided roads and restricted areas/lines.`

---

### 🤝 Get in Touch  
If you are interested in collaborating or discussing this project further, feel free to reach out via Slack:  
`nuril.hidayati`

---

### 🧠 ID Karta IoT Team – 2025  
🙏 *Special thanks to:*  
`Qitfirul, Mahardi Pratomo, Annisa Dwi Maiikhsantiani, and Mochammad Fachri.`
""")
