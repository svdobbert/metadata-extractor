from extract_metadata import process_dois, process_keywords


if __name__ == "__main__":
    input_csv = input("Enter the input CSV file path: ").strip()
    if not input_csv:
        input_csv = "./complete_list.csv"
    print(f"Using input CSV file: {input_csv}")
    
    output_csv = input("Enter the output CSV file path: ").strip()
    if not output_csv:
        output_csv = "./results.csv"
    print(f"Using output CSV file: {output_csv}")
    
    row_number_start = input("Enter the starting row number: ").strip()
    if not row_number_start:
        row_number_start = "1"
        
    row_number_end = input("Enter the ending row number: ").strip()
    if not row_number_end:
        row_number_end = "0"
    
    area_keywords = process_keywords("./keywords.csv")
    process_dois(input_csv, output_csv, area_keywords, row_number_start, row_number_end)