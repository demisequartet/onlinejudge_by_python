from json import dumps
import psycopg2
import os
from psycopg2.extras import DictCursor

print(psycopg2.apilevel)

DATABASE_URL = "postgresql://postgres:Password@localhost:5432/db"


def getCon():
    return psycopg2.connect(DATABASE_URL)


def strToFile(str):
    if os.path.exists("correct.txt"):
        os.remove("correct.txt")

    with open('correct.txt', 'w') as f:
        f.write(str)


def getCorrectOutput(question_id: int):
    conn = getCon()
    cur = conn.cursor()
    cur.execute(
        'SELECT output from question where question_id = {}'.format(question_id))
    for row in cur:
        print(row[0])
        print(type(row[0]))
    cur.close()
    conn.close()


def getALLQuestions() -> dict:
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * from question')
    results = cur.fetchall()
    dict_result = []
    for row in results:
        dict_result.append(dict(row))

    cur.close()
    conn.close()

    return dict_result


def main():
    conn = getCon()
    cur = conn.cursor()
    cur.execute('SELECT output from question')
    for row in cur:
        print(row[0])
        print(type(row[0]))
    cur.close()
    conn.close()


if __name__ == "__main__":
    # main()
    # getCorrectOutput(1)
    res = getALLQuestions()
    print(dumps(res))
