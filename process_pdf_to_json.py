import pdfplumber
import pandas as pd

# Step 1: Extract table content from the PDF
def extract_table_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        rows = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                rows.extend(table)
    return rows

# Step 2: Convert extracted data to a DataFrame, clean up column headers, and sort
def process_data_to_json(pdf_path, output_json_path):
    rows = extract_table_from_pdf(pdf_path)
    
    # Assuming the first row contains the column headers
    columns = rows[0]
    data = rows[1:]

    # Convert to pandas DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Replace "District" if it's in a different case (e.g., "district")
    district_col = [col for col in df.columns if col.lower() == "district"]
    if district_col:
        district_col = district_col[0]
    else:
        raise ValueError("No column named 'District' found.")

    # Step 3: Sort the DataFrame by the 'District' column
    df = df.sort_values(by=district_col)

    # Convert DataFrame to JSON and save it
    df.to_json(output_json_path, orient="records", indent=4)

# Execute the process
if __name__ == "__main__":
    pdf_path = "Copy-of-All-private-schools-as-at-28th-March-2022-1.pdf"
    output_json_path = "private_schools_sorted_by_district.json"
    
    try:
        process_data_to_json(pdf_path, output_json_path)
        print(f"Converted PDF to JSON and saved to {output_json_path}")
    except Exception as e:
        print(f"An error occurred: {e}")