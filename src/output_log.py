def output_log(str, end="\n"):
    print(str)
    with open("result/result.txt", "a") as f:
        print(str, end=end, file=f)
