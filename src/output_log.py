import re
import os

BASIC = True
DEBUG = True
TOO_MANY_OUTPUT = False

OUTPUT_FILE = None


def file_generator():
    path = "./result/"

    files = os.listdir(path)
    index = 0
    if files != []:
        for f in files:
            [base, extension] = f.split(".")
            if extension != "txt":
                print(f"Error: invalid extension: {base}.{extension}")
                break
            else:
                num = int(re.sub(r"\D", "", base))
                if num > index:
                    index = num
        else:
            index += 1

    return path + "result" + str(index) + ".txt"


def output_log(str, end="\n", output_flag=True):
    global OUTPUT_FILE
    if OUTPUT_FILE is None:
        OUTPUT_FILE = file_generator()

    if output_flag:
        print(str, end=end)
        with open(OUTPUT_FILE, "a") as f:
            print(str, end=end, file=f)
