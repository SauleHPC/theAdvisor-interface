import gzip
import sys

# prefix is where the files will be writte: {prefix}_{table}.sql.gz
def extract_tables(sql_file, tables, prefix):
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
                        file_name = f'{prefix}_{current_table}.sql.gz'
                        with gzip.open(file_name, 'at', encoding='utf-8') as outf:
                            outf.write(line)

                detected_encoding = encoding
                break
        except UnicodeDecodeError:
            continue

    if detected_encoding is None:
        print("Failed to detect encoding or decode file.")
        return

def usage ():
    print("Usage: python3 extractTable.py [sql_file] [prefix_output]")
    sys.exit(-1)


        
sql_file = '../../../mnt/large_data/csx_db_7_15_2014.sql.gz'
#tables_to_extract = ['citations']
tables_to_extract = ['citations', 'authors', 'papers', 'paperVersions' ]
prefix = 'csx_db_7_15_2014'

if len(sys.argv) > 1:
    if sys.argv[1] == '--help':
        usage()
    sql_file = sys.argv[1]
if len(sys.argv) > 2:
    prefix = sys.argv[2]

extract_tables(sql_file, tables_to_extract, prefix)
