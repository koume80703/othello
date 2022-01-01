BASIC = True
DEBUG = True
TOO_MANY_OUTPUT = False


def output_log(str, end="\n", output_flag=True):
    if output_flag:
        print(str, end=end)
        with open("result/result.txt", "a") as f:
            print(str, end=end, file=f)
