import streamlit as st
import pandas as pd
import csv
import ast

def flatten_coordinates_from_file(uploaded_file):
    if uploaded_file is None:
        st.warning("Please upload a CSV file.")
        return

    fieldnames = [
        "country_id", "id", "grid_id", "grid_id_clean", "road_coordinates",
        "first_coordinate", "created_at", "report_user_id", "type", "org_code", "note",
        "segment_id", "x", "y"
    ]

    output_rows = []
    try:
        # Read uploaded CSV as text lines
        decoded = uploaded_file.getvalue().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)

        for row in reader:
            try:
                coords_data = ast.literal_eval(row["road_coordinates"])

                if coords_data and isinstance(coords_data[0][0], (int, float)):
                    coords_data = [coords_data]

                for segment_index, segment_coords in enumerate(coords_data, start=1):
                    for coord in segment_coords:
                        output_rows.append({
                            "country_id": row.get("country_id", ""),
                            "id": row["id"],
                            "grid_id": row.get("grid_id", ""),
                            "grid_id_clean": row.get("grid_id_clean", ""),
                            "road_coordinates": row["road_coordinates"],
                            "first_coordinate": row.get("first_coordinate", ""),
                            "created_at": row.get("created_at", ""),
                            "report_user_id": row.get("report_user_id", ""),
                            "type": row.get("type", ""),
                            "org_code": row.get("org_code", ""),
                            "note": row.get("note", ""),
                            "segment_id": f"{row['id']}_{segment_index}",
                            "x": coord[0],
                            "y": coord[1],
                        })
            except Exception as e:
                st.error(f"Error processing row {row.get('id', 'unknown')}: {e}")

        # Convert to DataFrame and display
        df = pd.DataFrame(output_rows)
        st.dataframe(df)

        # Provide download button
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Flattened CSV",
            data=csv_data,
            file_name="flattened_coordinates.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Failed to process file: {e}")

# --- Streamlit UI ---
st.title("Flatten Coordinates CSV")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
if uploaded_file:
    flatten_coordinates_from_file(uploaded_file)
