import gzip

def extract_tables(sql_file, tables):
    encodings_to_try = ['utf-8']
    current_table = None

    for encoding in encodings_to_try:
        try:
            with gzip.open(sql_file, 'rt', encoding=encoding) as f:
                for line in f:
                    if line.startswith('INSERT INTO'):
                        #extract the table name from the SQL line
                        table_name = line.split()[2].strip('`')
                        
                        #check if the table is one we want to extract
                        if table_name in tables:
                            current_table = table_name
                        else:
                            current_table = None

                    if current_table is not None:
                        write_line(current_table, line)

                detected_encoding = encoding
                break
        except UnicodeDecodeError:
            continue

    if detected_encoding is None:
        print("Failed to detect encoding or decode file.")
        return

def write_line(table, line):
    file_name = f'csx_db_7_15_2014_{table}.sql.gz'
    with gzip.open(file_name, 'at', encoding='utf-8') as f:
        f.write(line)

sql_file = '../../../mnt/large_data/csx_db_7_15_2014.sql.gz'
tables_to_extract = ['citations']

extract_tables(sql_file, tables_to_extract)
