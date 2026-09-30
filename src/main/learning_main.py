from src.learning.learning import Learning

def main():
    learning = Learning(mode=0)
    learning.learning()

    learning = Learning(mode=1)
    learning.learning()


if __name__ == "__main__":
    main()