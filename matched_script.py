import csv
import pymongo

def read_csv(file_path):
    """Reads a CSV file and returns the headers and rows."""
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  
        rows = list(reader)  
    return headers, rows

def select_attributes_by_name(headers, hardcoded_attributes):
    """Automatically selects attributes based on the hardcoded list."""
    selected_indices = [headers.index(attr) for attr in hardcoded_attributes if attr in headers]  
    return selected_indices, hardcoded_attributes

def filter_rows(rows, selected_indices, selected_headers):
    """Filters the rows to include only the selected columns and returns them as dictionaries."""
    filtered_rows = []
    for row in rows:
        filtered_row = {selected_headers[i]: row[idx] for i, idx in enumerate(selected_indices)}
        filtered_rows.append(filtered_row)
    return filtered_rows

def write_to_mongodb(filtered_rows, collection):
    """Writes each filtered row (dictionary) as a separate document to MongoDB."""
    if filtered_rows:
        result = collection.insert_many(filtered_rows)  
        print(f"{len(result.inserted_ids)} documents inserted into MongoDB.")
    else:
        print("No data to insert into MongoDB.")

def main():
    input_file = "input.csv"  

    # MongoDB setup
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")  
    db = mongo_client["mydatabase"]  
    collection = db["mycollection"]  

    # Step 1: Read the original CSV file
    headers, rows = read_csv(input_file)

    # Step 2: Hardcoded attribute selection (e.g., only "title" and "_id")
    hardcoded_attributes = ["title", "_id"]  
    selected_indices, selected_headers = select_attributes_by_name(headers, hardcoded_attributes)

    # Step 3: Filter rows based on selected attributes
    filtered_rows = filter_rows(rows, selected_indices, selected_headers)

    # Step 4: Write the filtered data to MongoDB
    write_to_mongodb(filtered_rows, collection)

if __name__ == "__main__":
    main()
