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


def getALLsubmit():
    conn = getCon()
    cur = conn.cursor(cursor_factory=DictCursor)
    cur.execute(
        'SELECT * FROM  submit WHERE NOT (student_id = 98765432 OR student_id = 60230075)')
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

    acc = dict({"forwhile": 0, "for": 0, "while": 0})

    for submit in submits:
        if submit["result"] == "Accepted":
            if "for" in submit["source"] and "while" in submit["source"]:
                acc["forwhile"] += 1
            elif "for" in submit["source"]:
                acc["for"] += 1
            else:
                acc["while"] += 1

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
    import subprocess
    import re
    submits = getALLsubmit()
    a, b, c = 0, 0, 0

    for submit in submits:
        if submit["result"] == "Wrong Answer":
            with open("./temp.c", "w") as f:
                f.write(str(submit["source"]) + "\n")
            command = "gcc {}".format("temp.c")

            cp = subprocess.run(command, shell=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            cp2 = subprocess.run("./a.out", shell=True,
                                 stdin=open(f'input.txt', "r"),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            print(cp2.stdout.decode())

            stdout = re.sub('[^0-9]', '', cp2.stdout.decode())

            if stdout == "123246369":
                print(f'{submit["student_id"]}九九ok')
                a += 1
            else:
                if stdout:
                    print(f'{submit["student_id"]}九九ng')
                    b += 1
                else:
                    print(f'{submit["student_id"]}NG')
                    c += 1

                    # if not str(cp2.stdout).count(",", 12):
                    #     print("comma error")
                    # elif not str(cp2.stdout).count("\n", 3):
                    #     print("line error")
                    # else:
                    #     print("other error")

                    # temp.c a.outが存在するなら削除
    if os.path.exists("./temp.c"):
        os.remove("./temp.c")
    if os.path.exists("./a.out"):
        os.remove("./a.out")

    print(f'九九ok{a}九九ng{b}NG{c}')


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
    print(f'一回の提出でAcceptした人{len(superaccepter)}')
    print(
        f'一回の提出でAcceptしなかった人がAcceptするまでに間違う平均回数{sum(notsuperaccepter)/len(notsuperaccepter)}')


if __name__ == "__main__":
    # ansanalyzer()

    # AcceptedSourceAnalyzer()

    # analyzer()

    WrongAnswerAnalyzer()
