def output_log(str):
    print(str)
    with open("result/result.txt", "a") as f:
        print(str, file=f)
