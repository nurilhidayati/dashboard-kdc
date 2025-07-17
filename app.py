import streamlit as st

st.set_page_config(
    page_title="Analyst Gap Justification",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

st.title("🛠️ Analyst Gap Justification")

st.markdown("""
### 🔍 Overview

**Analyst Gap Justification** is a web-based geospatial tool built with Streamlit.  
It helps analyze road segments that may pass through **restricted zones** by letting you:

- Upload and clean coordinate data
- Visualize road geometry on a map
- Download restricted areas from OpenStreetMap (OSM)
- Run spatial analysis to find overlaps

---

### 🔄 Workflow Steps
**✅ Step 1: Split Data Per City**  
This step filters and extracts rows from the uploaded CSV file based on a specific city name found within the grid_id column. The application identifies the city by splitting the grid_id string and matching the second word with the city name you enter (e.g., "Jakarta"). This is useful when you only want to analyze or export data from a particular city out of a larger dataset.


**✅ Step 2: Flatten Coordinates**  
Raw coordinate data often looks like this:  
`[[(104.75, -2.97), (104.76, -2.96)]]`  

This format stores multiple coordinates in one row, making them hard to use.

**Why this matters:**  
- Breaks grouped points into one row per coordinate  
- Prepares data for drawing roads  
- Makes it easier to spot missing or incorrect points  

**Analogy:**  
Imagine a tangled string of dots — this step lays them out clearly so you can connect them.

📥 Start by uploading a CSV file containing grouped coordinates.

---

**✏️ Step 3: Convert to Polylines**  
After flattening, each road is still just a list of dots.  
We now **connect the dots** to form visible road paths.

**Why this matters:**  
- Transforms points into lines (polylines)  
- Allows roads to be displayed on a map  
- Essential for checking if roads cross restricted areas  

**Analogy:**  
Dots A → B → C are just locations — but connecting them creates an actual road.

---

**🌍 Step 4: Download Restricted Areas**  
This step fetches restricted zones from OpenStreetMap, such as:
- 🚫 Military or industrial zones  
- 🛣️ Roads with private or limited access  

**Why this matters:**  
- Adds background layers for spatial comparison  
- Tells the tool where roads **shouldn't** go  

**Analogy:**  
Before planning your route, you need to know where entry is not allowed.  
This step maps those "no-go zones."

---

**🚧 Step 5: Find Intersections**  
Now we check: do any roads **intersect** with restricted zones?

**Why this matters:**  
- Highlights road segments inside or near restricted areas  
- Helps avoid routing errors or violations  
- Produces a clean GeoJSON output for further use

**Analogy:**  
Think of it as drawing a red flag where a road touches a danger zone.

---

### 💬 Contact & Credits

📩 **Slack contact:** `nuril.hidayati`  
👥 **Project Team:** ID Karta IoT – 2025  
🙏 **Thanks to:** Qitfirul, Mahardi Pratomo, Annisa Dwi Maiikhsantiani, and Mochammad Fachri
""")
