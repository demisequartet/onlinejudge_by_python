import psycopg2

print(psycopg2.apilevel)

DATABASE_URL = "postgresql://postgre:postgre@localhost:5432/postgres"


def main():
    cursor = psycopg2.connect(DATABASE_URL)
    print(cursor)


if __name__ == "__main__":
    main()
