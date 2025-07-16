import streamlit as st
import pandas as pd
import csv
import ast
import io

st.title("Flatten Road Coordinates CSV Tool")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    try:
        # Read uploaded CSV
        df = pd.read_csv(uploaded_file)

        output_fieldnames = [
            "country_id", "id", "grid_id", "grid_id_clean", "road_coordinates",
            "first_coordinate", "created_at", "report_user_id", "type", "org_code", "note",
            "segment_id", "x", "y"
        ]

        # Use StringIO to write CSV to memory
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=output_fieldnames)
        writer.writeheader()

        for index, row in df.iterrows():
            try:
                coords_data = ast.literal_eval(row["road_coordinates"])

                if coords_data and isinstance(coords_data[0][0], (int, float)):
                    coords_data = [coords_data]

                for segment_index, segment_coords in enumerate(coords_data, start=1):
                    for coord in segment_coords:
                        writer.writerow({
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
                st.warning(f"⚠️ Error processing row {row.get('id', 'unknown')}: {e}")

        # Convert string buffer to downloadable CSV
        st.success("✅ CSV processed successfully!")
        processed_csv = output.getvalue()
        st.download_button("⬇️ Download Flattened CSV", processed_csv, file_name="2024campaign.csv", mime="text/csv")

        # Show preview
        output.seek(0)
        df_output = pd.read_csv(output)
        st.dataframe(df_output.head())

    except Exception as e:
        st.error(f"❌ Error: {e}")
