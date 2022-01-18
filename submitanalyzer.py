from json import dumps
import psycopg2
import os
from psycopg2.extras import DictCursor
import urllib.parse
import csv

# print(psycopg2.apilevel)

DATABASE_URL = "postgresql://postgres:Password@localhost:5432/db"
# DATABASE_URL = "postgresql://postgres:Password@db-container:5432/db"


def getCon():
    return psycopg2.connect(DATABASE_URL)


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
    cur.execute(
        'SELECT * FROM  submit WHERE NOT (student_id = 98765432 OR student_id = 60236163)')
    submits = []

    for i in cur:
        submits.append(dict(i))

    cur.close()
    conn.close()

    return submits


def getResponseID(studentID, questionID, result, source):
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute('SELECT response_id FROM submit WHERE student_id = %s AND question_id = %s AND result = %s AND source = %s',
                (studentID, questionID, result, source))
    res = cur.fetchone()
    cur.close()
    conn.close()
    return dict(res)["response_id"]


def analyzer():
    submits = getALLsubmit()
    # print(submits)

    print(f'総提出数{len(submits)}')

    stuid = dict()

    res = dict()

    for submit in submits:
        if submit["student_id"] not in stuid:
            stuid[submit["student_id"]] = 1
        else:
            stuid[submit["student_id"]] += 1
    print(sorted(stuid.items(), key=lambda x: x[0], reverse=True))

    for submit in submits:
        if submit["result"] not in res:
            res[submit["result"]] = 1
        else:
            res[submit["result"]] += 1

    print(sorted(res.items(), key=lambda x: x[1], reverse=True))

    print(f'オンラインジャッジ利用者数{len(stuid)}')


def AcceptedSourceAnalyzer():
    submits = getALLsubmit()

    acc = dict({"for": 0, "while": 0, "other": 0})

    for submit in submits:
        if submit["result"] == "Accepted":
            if "for" in submit["source"]:
                acc["for"] += 1
            elif "while" in submit["source"]:
                acc["while"] += 1
            else:
                acc["other"] += 1

    print(acc)


def CompileErrorSourceAnalyzer():
    submits = getALLsubmit()

    source = []

    for submit in submits:
        if submit["result"] == "Compile Error":
            source.append([submit["student_id"], submit["source"]])

    for i, con in enumerate(source):
        with open(f"submit/compileError{i}.c", "w") as f:
            f.write(str(con[1]) + "\n")


def WrongAnswerAnalyzer():
    submits = getALLsubmit()

    source = []

    for submit in submits:
        if submit["result"] == "Wrong Answer":
            if "for" in submit["source"] or "while" in submit["source"]:
                source.append([submit["student_id"], submit["source"]])

    for i, con in enumerate(source):
        with open(f"submit/wrongans{i}.c", "w") as f:
            f.write(str(con[1]) + "\n")


def makeCSV():
    submits = getALLsubmit()

    label = submits[0].keys()

    with open("data.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=label)
        writer.writeheader()
        for i in submits:
            writer.writerow(i)


def ansanalyzer():
    submits = getALLsubmit()

    student_ids = set()

    for submit in submits:
        student_ids.add(submit["student_id"])

    res = []

    for id in student_ids:
        tempres = {"id": id, "Accepted": 0,
                   "Wrong Answer": 0, "Compile Error": 0}
        for submit in submits:
            if submit["student_id"] == id:
                if submit["result"] == "Accepted":
                    tempres["Accepted"] += 1
                elif submit["result"] == "Wrong Answer":
                    tempres["Wrong Answer"] += 1
                elif submit["result"] == "Compile Error":
                    tempres["Compile Error"] += 1
        res.append(tempres)

    ac, wa = 0, 0

    for i in res:
        if i["Accepted"] != 0:
            ac += 1
        else:
            wa += 1

    print(ac, wa)
    print(ac/(ac+wa))
    res.sort(key=lambda x: x["Accepted"])

    superaccepter, notsuperaccepter = [], []

    for i in res:
        if i["Accepted"] != 0:
            if i["Wrong Answer"] + i["Compile Error"] == 0:
                superaccepter.append(i["id"])
            else:
                notsuperaccepter.append(i["Wrong Answer"] + i["Compile Error"])
    print(len(superaccepter))
    print(sum(notsuperaccepter)/len(notsuperaccepter))


if __name__ == "__main__":
    # AcceptedSourceAnalyzer()
    # CompileErrorSourceAnalyzer()
    # WrongAnswerAnalyzer()
    # makeCSV()
    ansanalyzer()
