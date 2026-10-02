from src.library.result.result_generate import Result_generate


def generate_result(result_name):
    result = Result_generate(result_name)
    result.generate()


def generate_best_result():
    result = Result_generate.get_best_result()
    result.generate()


def main():
    print("1: Result名を指定")
    print("2: Accuracy最大のResultを使用")

    mode = input("選択: ")

    if mode == "1":
        result_name = input("Result名: ")
        generate_result(result_name)

    elif mode == "2":
        generate_best_result()

    else:
        print("不正な選択です")


if __name__ == "__main__":
    main()