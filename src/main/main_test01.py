from src.learning.learning import Learning


def main():
    learning = Learning(0)

    learning.data_create()
    learning.file_read()
    learning.learning()


if __name__ == "__main__":
    main()