import psycopg2
import csv
from decouple import config

dbname = config ('dbname')
user = config ('user')
password = config ('password')
host = config ('host')
port = config ('port')
table_name = config ('table_name')
data_csv_file = config ('data_csv_file')
try:

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]
    with open(data_csv_file, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names)
        for row in rows:
            csv_writer.writerow(row)
    print(f"Data from table '{table_name}' has been exported to '{data_csv_file}'")
except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL or exporting data:", error)
finally:
    if conn:
        cursor.close()
        conn.close()
        print("PostgreSQL connection is closed")