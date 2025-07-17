import csv
import ast
import pandas as pd

def flatten_coordinates(input_csv_path, output_csv_path):
    """
    Reads a CSV with 'road_coordinates' column containing nested coordinate lists,
    flattens coordinates into separate rows with x and y columns,
    and writes the output to a new CSV.
    """
    fieldnames = [
        "country_id", "id", "grid_id", "grid_id_clean", "road_coordinates",
        "first_coordinate", "created_at", "report_user_id", "type", "org_code", "note",
        "segment_id", "x", "y"
    ]

    with open(input_csv_path, mode="r", encoding="utf-8") as infile, \
         open(output_csv_path, mode="w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            try:
                coords_data = ast.literal_eval(row["road_coordinates"])

                # Normalize: if single segment (list of tuples), wrap in list
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
                print(f"⚠️ Error processing row {row.get('id', 'unknown')}: {e}")

    print(f"✅ Flattened coordinates saved to: {output_csv_path}")

    # Optional: preview first 5 rows
    df = pd.read_csv(output_csv_path)
    print(df.head())

# Example usage:
flatten_coordinates(
    input_csv_path="/content/ID_Gap Justification_2024 - Palembang.csv",
    output_csv_path="2024campaign.csv"
)
