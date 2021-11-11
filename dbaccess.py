import psycopg2

print(psycopg2.apilevel)

DATABASE_URL = "postgresql://postgres:Password@localhost:5432/db"


def getCon():
    return psycopg2.connect(DATABASE_URL)


def main():
    conn = getCon()
    cur = conn.cursor()
    cur.execute('SELECT output from question')
    for row in cur:
        print(row)
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
