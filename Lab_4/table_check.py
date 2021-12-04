import psycopg2
conn = psycopg2.connect(dbname='d35ghu4nho8g46', user='noglraoqozczqg',
                        password='c3e7c74e860567d660bf4b365f5b400e9f7611d023fbc051d4b7a2cbef695833', host='ec2-54-247-122-209.eu-west-1.compute.amazonaws.com')

print("Database opened successfully")

cur = conn.cursor()
# cur.execute("CREATE TABLE forlab4 (id SERIAL PRIMARY KEY, " +
#     "from_ VARCHAR(4), value_ VARCHAR(20), to_ VARCHAR(4), res_ VARCHAR(10))")
# conn.commit()

cur.execute("SELECT id, from_, value_, to_ FROM forlab4")
for row in cur:
    print(row)

cur.close()
conn.close()