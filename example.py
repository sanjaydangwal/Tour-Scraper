import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)

new_rows = [('Cats', 'Cat City', '2088.10.17'),
            ('Hens', 'Hen City', '2088.10.17')]

cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)
connection.commit()