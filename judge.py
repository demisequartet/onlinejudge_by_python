import os
import subprocess
from hashlib import sha256


def main(str):
    result = ""

    if "system" in str:
        return "Dangerous Program"

    stringToFile(str)
    if os.path.isfile("./submit.c"):

        result = compile("submit.c")
        deleteBinary()

    return result


def stringToFile(str):
    f = open("submit.c", "w")
    f.write(str)
    f.close()


def compile(FileName):
    command = "gcc {}".format(FileName)

    cp = subprocess.run(command, shell=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if cp.returncode != 0:
        return "Compile Error"

    return func()


def func():
    command = "./a.out"

    try:
        # refer https://docs.python.org/ja/3/library/subprocess.html
        cp = subprocess.run(command, shell=False,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2, check=True)

        stdout = cp.stdout.decode("utf-8")
    except subprocess.TimeoutExpired:
        # print("Time Limit Exceeded")
        return "Time Limit Exceeded"
    except subprocess.CalledProcessError:
        # print("Runtime Error")
        return "Runtime Error"
    else:
        return answerJudge(stdout)


def answerJudge(stdout):
    stdout = answerEndlineDeleter(stdout)
    print(stdout)
    stdout = stdout.encode("utf-8")
    submitHash = sha256(stdout).hexdigest()

    ans = open("correct.txt", "r").read()
    ans = answerEndlineDeleter(ans)
    ans = ans.encode("utf-8")
    print(ans)

    ansHash = sha256(ans).hexdigest()

    if submitHash == ansHash:
        # print("Accepted")
        return "Accepted"
    else:
        # print("Wrong Answer")
        return "Wrong Answer"


def answerEndlineDeleter(str):
    while str[-1] == "\n":
        str = str[:-1]

    return str


def deleteBinary(FileName="./a.out"):
    if os.path.isfile(FileName):
        os.remove(FileName)


if __name__ == "__main__":
    FileName = ["accepted.c", "wronganswer.c",
                "RuntimeError.c", "CompileError.c", "endlessloop.c", "dangerous.c"]

    for file in FileName:
        file = "./testFile/" + file
        print(file + " test")
        print(compile(file))
        deleteBinary()

    teststr = "abcdefgh\nfjfjf\n\n\n\n"
    print(teststr)

    teststr = answerEndlineDeleter(teststr)

    print(teststr)
