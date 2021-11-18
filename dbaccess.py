from json import dumps
import psycopg2
import os
from psycopg2.extras import DictCursor
import urllib.parse

print(psycopg2.apilevel)

# DATABASE_URL = "postgresql://postgres:Password@localhost:5432/db"
DATABASE_URL = "postgresql://postgres:Password@db-container:5432/db"


def getCon():
    return psycopg2.connect(DATABASE_URL)


def outputTofile(num):
    conn = getCon()
    cur = conn.cursor()
    cur.execute('SELECT output from question where question_id = %s', (num,))
    output = cur.fetchone()[0]
    cur.close()
    conn.close()

    print(output)

    strToFile(output)


def strToFile(str):
    if os.path.exists("correct.txt"):
        os.remove("correct.txt")

    with open('correct.txt', 'w') as f:
        f.write(str)


def getCorrectOutput(question_id: int):
    conn = getCon()
    cur = conn.cursor()
    cur.execute(
        'SELECT output from question where question_id = %s', (question_id,))
    for row in cur:
        print(row[0])
        print(type(row[0]))
    cur.close()
    conn.close()


def getQuestion(num: int) -> dict:
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * from question where question_id = %s', (num,))

    res = dict(cur.fetchone())

    cur.close()
    conn.close()

    return res


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


def registerSource(student_id: int, question_id: int, result: str, source: str):
    conn = getCon()
    cur = conn.cursor()
    cur.execute("INSERT INTO submit(student_id,question_id,result,source) VALUES (%s,%s,%s,%s)",
                (student_id, question_id, result, source,))

    conn.commit()  # https://www.psycopg.org/docs/connection.html?highlight=commit#connection.commit
    cur.close()
    conn.close()


def getALLsubmit():
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT * FROM submit')
    submits = []

    for i in cur:
        submits.append(dict(i))

    cur.close()
    cur.close()
    conn.close()

    return submits


if __name__ == "__main__":
    # registerSource(1, 1, "a", "b")
    print(getALLsubmit())
