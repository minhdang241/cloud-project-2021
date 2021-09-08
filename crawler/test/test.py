import psycopg2

conn = psycopg2.connect(
    dbname="cloud",
    user="postgres",
    password="nB7geYEjbFT3UBUKJqfKkPuHpkKsUVsWmaDcrTdd6d6HpkKsUVsWmDaQDxJqfKkPu",
    host="localhost",
    port="10000",
)

cur = conn.cursor()

cur.execute('select * from "Careers"')

rows = cur.fetchall()
print(rows)